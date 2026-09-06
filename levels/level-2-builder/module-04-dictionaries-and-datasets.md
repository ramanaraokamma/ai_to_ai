# Module 4 — Dictionaries and Datasets: Your First Data in Code

**Level 2 · Module 4 · ~4 hours · Prereqs: Modules 1–3 (variables, types, f-strings, if/elif/else, loops, functions with `return`, lists, list comprehensions, importing your own module)**

[⬅ Previous](module-03-functions-and-lists.md) · [Level 2 Home](README.md) · [Next ➡](module-05-numpy-arrays.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** create and update dictionaries, and access values safely with `.get()` instead of crashing on a missing key.
2. **You will be able to** represent a whole dataset as a **list of dictionaries** with consistent keys — one dict per row, keys as columns.
3. **You will be able to** write your own `filter_by()` and `group_count()` functions that work on *any* dataset, not just one.
4. **You will be able to** store a dict inside a dict (nested data) and reach into it two levels deep.
5. **You will be able to** write a dataset to a CSV file with `csv.DictWriter`, read it back with `csv.DictReader`, and explain why every value comes back as text.

---

## 🪝 The Hook

In Module 3 you built a Stats Toolkit and fed it twenty cricket scores:

```python
scores = [45, 12, 88, 0, 103, 7, 61, 34, 90, 22, 55, 17, 76, 41, 8, 68, 29, 95, 13, 50]
```

Here is a question that list cannot answer: **who scored the 103?**

You know somebody did. The number is right there. But the list stores only numbers, and a number does not remember whose it was. It doesn't remember the date, or the ground, or whether the team won. All of that got thrown away the moment you typed the list.

A list is a row of lockers with numbers on them: locker 0, locker 1, locker 2. A **dictionary** is a row of lockers with *names* on them: `"player"`, `"runs"`, `"ground"`. Once your lockers have names, one locker set can hold one whole cricket innings — and a *list of those* is a table. That's a dataset. That is the thing every model in this level will eat.

---

## 🧠 The Concept

### 1. Dictionaries: keys, values, `.get()`, `.items()`, and `KeyError`

#### The plain-language explanation

A **dictionary** is a container that stores pairs: a *key* you look things up by, and a *value* you get back.

> **Definition — dictionary (`dict`):** a collection of `key: value` pairs where you fetch a value by naming its key, not by counting positions.

> **Definition — key:** the label you look a value up by. Almost always a string in this course.

> **Definition — value:** the thing stored under a key. Can be any type — number, string, list, even another dictionary.

You write one with curly braces `{}` and colons between key and value:

```python
player = {"name": "Ishaan", "runs": 103, "out": False}
```

Read it out loud: *"under the key `name` is `Ishaan`; under `runs` is `103`; under `out` is `False`."*

#### 🍕 The analogy

Think of the index cards you might use to organise a shelf of books. A list is the shelf: book 0, book 1, book 2 — you find a book by counting along. A dictionary is the card catalogue: you don't count, you *ask by name*. "Where's the book about volcanoes?" You go straight to the V card.

Counting works fine until someone inserts a book in the middle and every number shifts. Names don't shift.

#### 🔍 Tiny concrete example

```python
player = {"name": "Ishaan", "runs": 103, "out": False}

print(player["name"])        # Ishaan   — square brackets, but a KEY not a number
print(player["runs"])        # 103
print(len(player))           # 3        — three key:value pairs
```

**Adding and changing.** You do both the same way — assign to a key:

```python
player["runs"] = 110         # key already exists → CHANGES the value
player["ground"] = "Chinnaswamy"   # key is new    → ADDS a new pair
print(player)
```

Output:

```
{'name': 'Ishaan', 'runs': 110, 'out': False, 'ground': 'Chinnaswamy'}
```

Notice the new pair went on the end. Since Python 3.7, a dictionary **remembers the order you inserted keys in**. That's handy and you can rely on it.

**Removing:**

```python
del player["out"]            # removes the key AND its value
print(player)
```

```
{'name': 'Ishaan', 'runs': 110, 'ground': 'Chinnaswamy'}
```

#### The crash you will meet: `KeyError`

Ask for a key that isn't there and Python stops the program:

```python
print(player["age"])
```

```
Traceback (most recent call last):
  File "cards.py", line 8, in <module>
    print(player["age"])
          ~~~~~~^^^^^^^
KeyError: 'age'
```

> **Definition — `KeyError`:** the error Python raises when you ask a dictionary for a key it does not have.

Just like the tracebacks in Module 1: read the last line first (`KeyError: 'age'`), then the line number.

#### `.get()` — the safe way to ask

`.get(key)` asks the same question but returns `None` instead of crashing. `.get(key, default)` returns a fallback you choose.

```python
print(player.get("age"))          # None      — no crash
print(player.get("age", 0))       # 0         — your chosen fallback
print(player.get("runs", 0))      # 110       — key exists, so you get the real value
```

| You write | Key exists | Key missing |
|---|---|---|
| `d["k"]` | returns the value | 💥 `KeyError`, program stops |
| `d.get("k")` | returns the value | returns `None` |
| `d.get("k", 0)` | returns the value | returns `0` |

**Rule of thumb:** use `d["k"]` when a missing key means your data is broken and you *want* to know loudly. Use `d.get("k", default)` when a missing key is normal and you have a sensible fallback. Real datasets have holes, so you will use `.get()` a lot.

#### Looping over a dictionary: `.keys()`, `.values()`, `.items()`

```python
player = {"name": "Ishaan", "runs": 110, "ground": "Chinnaswamy"}

for k in player.keys():
    print(k)
# name
# runs
# ground

for v in player.values():
    print(v)
# Ishaan
# 110
# Chinnaswamy

for k, v in player.items():          # ← the one you'll use 90% of the time
    print(f"{k}: {v}")
# name: Ishaan
# runs: 110
# ground: Chinnaswamy
```

> **Definition — `.items()`:** gives you both the key and the value on each loop turn, as a pair you unpack into two variables.

Two more useful checks:

```python
print("runs" in player)      # True   — 'in' checks KEYS, not values
print(110 in player)         # False  — 110 is a value, not a key
print(110 in player.values())  # True
```

---

### 2. List-of-dicts as a table: one dict = one row, keys = columns

#### The plain-language explanation

One dictionary describes **one thing**. Put many of those dictionaries in a list and you have **many things described the same way** — which is exactly what a table is.

> **Definition — record:** one dictionary describing one thing (one song, one student, one match). Same as one row of a table.

> **Definition — dataset (list of dicts):** a list where every element is a record and every record uses the same keys.

#### 🍕 The analogy

Imagine a shoebox of index cards, one card per song in your library. Every card has the same six printed labels: *Title, Artist, Genre, Minutes, Plays*. Fill in the blanks and you can flick through the whole box comparing like with like.

The rule that makes the box useful is boring and absolute: **every card has the same labels.** If one card says *Singer* instead of *Artist*, every program you write has to special-case it forever.

#### 🔍 Tiny concrete example

Here is the six-song dataset we'll use for the rest of the module. Type it out; you'll need it.

```python
songs = [
    {"title": "Blue Lights",  "artist": "Nova",  "genre": "pop",  "minutes": 3.5, "plays": 120},
    {"title": "Rain Check",   "artist": "Kabir", "genre": "rock", "minutes": 4.2, "plays": 45},
    {"title": "Ghost Town",   "artist": "Nova",  "genre": "pop",  "minutes": 2.8, "plays": 300},
    {"title": "Slow Train",   "artist": "Meera", "genre": "folk", "minutes": 5.1, "plays": 60},
    {"title": "Neon Streets", "artist": "Kabir", "genre": "rock", "minutes": 3.9, "plays": 210},
    {"title": "Paper Boats",  "artist": "Nova",  "genre": "pop",  "minutes": 3.3, "plays": 95},
]
```

Here is the same thing drawn as the table it actually is:

```
                       COLUMNS  =  the keys
             ┌──────────┬────────┬───────┬─────────┬───────┐
             │  title   │ artist │ genre │ minutes │ plays │
   ┌─────────┼──────────┼────────┼───────┼─────────┼───────┤
 R │songs[0] │Blue Lights  Nova     pop      3.5      120  │  ← one dict
 O │songs[1] │Rain Check   Kabir    rock     4.2       45  │  ← one dict
 W │songs[2] │Ghost Town   Nova     pop      2.8      300  │  ← one dict
 S │songs[3] │Slow Train   Meera    folk     5.1       60  │  ← one dict
   │songs[4] │Neon Streets Kabir    rock     3.9      210  │  ← one dict
   │songs[5] │Paper Boats  Nova     pop      3.3       95  │  ← one dict
   └─────────┴──────────┴────────┴───────┴─────────┴───────┘

   songs          → the whole list (the table)
   songs[2]       → one record (a dict)          {"title": "Ghost Town", ...}
   songs[2]["plays"] → one cell                  300
```

Two indexing steps, and they mean different things:

```python
print(songs[2])              # {'title': 'Ghost Town', 'artist': 'Nova', ...}
print(songs[2]["plays"])     # 300     ← list index first, then dict key
print(len(songs))            # 6       ← number of ROWS
print(len(songs[0]))         # 5       ← number of COLUMNS
```

And you can loop over rows exactly as you looped over lists in Module 3:

```python
for song in songs:
    print(f"{song['title']:<14} {song['plays']:>4} plays")
```

Output:

```
Blue Lights     120 plays
Rain Check       45 plays
Ghost Town      300 plays
Slow Train       60 plays
Neon Streets    210 plays
Paper Boats      95 plays
```

> ⚠️ Notice the quote juggling inside the f-string: the f-string uses double quotes, so inside `{}` the key uses **single** quotes: `{song['title']}`. Mixing them up is the #1 typo in this module.

Extracting one column is a list comprehension — the tool you built in Module 3:

```python
all_plays = [s["plays"] for s in songs]
print(all_plays)             # [120, 45, 300, 60, 210, 95]
print(sum(all_plays))        # 830
print(max(all_plays))        # 300
```

---

### 3. Filtering records, and grouping with a counting dictionary

#### The plain-language explanation

Two questions dominate all data work:

- **"Show me only the rows where ___."** → that's **filtering**.
- **"How many rows of each kind are there?"** → that's **grouping**.

> **Definition — filter:** keep only the records that pass a test; throw the rest away. The result is a smaller list of the same shape.

> **Definition — group and count:** sort records into buckets by the value of one key, and report the size of each bucket.

#### 🍕 The analogy

Filtering is a sieve. You tip the whole box of song cards through, and only the pop songs fall out the bottom. What comes out is still a box of cards, just fewer of them.

Grouping is sorting laundry. You don't throw anything away; you make a pile per colour and then count each pile. The counting dictionary *is* the set of piles — one key per pile, one number per pile.

#### 🔍 Tiny concrete example — filtering

```python
def filter_by(records, key, value):
    """Return the records whose `key` equals `value`."""
    kept = []                          # start an empty result list
    for r in records:                  # look at every record
        if r.get(key) == value:        # .get() so a missing key is False, not a crash
            kept.append(r)             # passed the test → keep it
    return kept                        # hand back the smaller list

pop = filter_by(songs, "genre", "pop")
print(len(pop))                        # 3
for s in pop:
    print(s["title"])
```

Output:

```
3
Blue Lights
Ghost Town
Paper Boats
```

The same thing as a one-line comprehension — identical meaning, shorter:

```python
def filter_by(records, key, value):
    return [r for r in records if r.get(key) == value]
```

Notice what makes this function *good*: it doesn't know anything about songs. Pass it students and `"grade"`, `"8A"` and it works. That's the payoff of Module 3's lesson — write the tool, not the one-off.

#### 🔍 Tiny concrete example — the counting dictionary

The **counting dictionary** pattern is worth memorising, because you will type it for the rest of your life:

```python
def group_count(records, key):
    """Count how many records share each value of `key`."""
    counts = {}                          # empty dict of buckets
    for r in records:
        value = r.get(key, "MISSING")    # missing key gets its own bucket
        counts[value] = counts.get(value, 0) + 1   # ← THE line
    return counts

print(group_count(songs, "genre"))
print(group_count(songs, "artist"))
```

Output:

```
{'pop': 3, 'rock': 2, 'folk': 1}
{'Nova': 3, 'Kabir': 2, 'Meera': 1}
```

**Unpack THE line**, because it does two jobs at once:

```python
counts[value] = counts.get(value, 0) + 1
#               └──────────┬────────┘
#         "the count so far, or 0 if we've never seen this value"
```

- First time we see `"pop"`: `counts.get("pop", 0)` → `0`, so `counts["pop"] = 1`.
- Second time: `counts.get("pop", 0)` → `1`, so `counts["pop"] = 2`.

Without `.get()` you'd need four lines and an `if`:

```python
if value in counts:
    counts[value] = counts[value] + 1
else:
    counts[value] = 1
```

Same result. The `.get()` version is why `.get()` exists.

**Sorting the buckets** so the biggest is first — `sorted()` on `.items()`:

```python
counts = group_count(songs, "genre")
ordered = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
print(ordered)          # [('pop', 3), ('rock', 2), ('folk', 1)]
```

> **Definition — `lambda`:** a tiny throwaway function written on one line. `lambda pair: pair[1]` means "given a pair, hand back item 1 of it" — here, the count. `sorted` uses that number to decide the order.

You don't need to master `lambda` today. Just recognise the shape: *sort these pairs by their second element, biggest first.*

---

### 4. Nested data: a dict inside a dict

#### The plain-language explanation

A value in a dictionary can be *anything* — including another dictionary, or a list.

> **Definition — nested data:** data with containers inside containers, so you need more than one lookup step to reach a value.

#### 🍕 The analogy

A school's student records aren't one flat card. There's a card for the student, and stapled to it is a smaller card for the emergency contact, and a strip listing their clubs. To reach the contact's phone number you open the student card *first*, then the contact card. Two steps, in order.

#### 🔍 Tiny concrete example

```python
artists = {
    "Nova": {
        "country": "India",
        "started": 2019,
        "members": ["Anya", "Rehan"],
    },
    "Kabir": {
        "country": "UK",
        "started": 2016,
        "members": ["Kabir"],
    },
}

print(artists["Nova"]["country"])        # India
print(artists["Nova"]["members"])        # ['Anya', 'Rehan']
print(artists["Nova"]["members"][0])     # Anya
print(len(artists["Kabir"]["members"]))  # 1
```

Read `artists["Nova"]["members"][0]` strictly **left to right**:

```
artists                          → the outer dict
artists["Nova"]                  → {'country': 'India', 'started': 2019, 'members': [...]}
artists["Nova"]["members"]       → ['Anya', 'Rehan']
artists["Nova"]["members"][0]    → 'Anya'
```

If any step is missing you get a `KeyError` on *that* step. Chained `.get()` protects you, but read it carefully:

```python
print(artists.get("Meera", {}).get("country", "unknown"))   # unknown
```

`artists.get("Meera", {})` returns an **empty dict** when Meera isn't there, and an empty dict is still a dict, so the second `.get()` is legal and returns `"unknown"`. The empty-dict default is a small trick that saves a lot of crashes.

Looping over nested data needs a nested loop:

```python
for name, info in artists.items():
    print(f"{name} ({info['country']}, since {info['started']})")
    for member in info["members"]:
        print(f"    - {member}")
```

Output:

```
Nova (India, since 2019)
    - Anya
    - Rehan
Kabir (UK, since 2016)
    - Kabir
```

#### When to nest and when not to

Nesting is powerful and easy to overuse. Here's the honest guidance:

| Situation | Shape to use |
|---|---|
| Many things, all described the same way | **List of flat dicts** (a table) |
| One thing with sub-details you rarely loop over | Dict with a nested dict |
| Anything you plan to save as CSV | **Flat dicts only** — CSV has no way to store nesting |

That last row matters in about ten minutes. CSV files are flat grids. A nested dict cannot go into one cell without being mangled.

---

### 5. CSV files: `csv.DictWriter`, `csv.DictReader`, and why everything reads back as text

#### The plain-language explanation

Your dataset lives inside a running program. Close the program and it's gone. To keep it, write it to a **file** — and the universal file format for tables is CSV.

> **Definition — CSV (Comma-Separated Values):** a plain text file where the first line names the columns and every later line is one row, with commas between the fields.

Our six songs as CSV text:

```
title,artist,genre,minutes,plays
Blue Lights,Nova,pop,3.5,120
Rain Check,Kabir,rock,4.2,45
Ghost Town,Nova,pop,2.8,300
Slow Train,Meera,folk,5.1,60
Neon Streets,Kabir,rock,3.9,210
Paper Boats,Nova,pop,3.3,95
```

That's it. No fonts, no colours, no formulas — just text. Every spreadsheet program on Earth opens it, and so does pandas in Module 6.

#### 🍕 The analogy

CSV is a postcard. You can write anything you like on it, but only as writing. You can't post a Lego brick. When your data arrives it is *all handwriting* — including the bit that used to be a number.

#### 🔍 Writing with `csv.DictWriter`

```python
import csv

fieldnames = ["title", "artist", "genre", "minutes", "plays"]

with open("songs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()          # writes the first line: title,artist,genre,...
    writer.writerows(songs)       # writes one line per dict
```

Line by line:

| Piece | What it does |
|---|---|
| `open(path, "w")` | opens the file for **w**riting; an existing file is erased |
| `newline=""` | stops Windows from inserting a blank line between rows. Always include it with `csv`. |
| `encoding="utf-8"` | lets names with accents or non-English scripts save correctly |
| `with ... as f:` | guarantees the file gets closed even if the code crashes |
| `fieldnames=` | fixes the column order *and* which keys get written |
| `.writeheader()` | writes the header row. Forget it and your first song becomes the header. |
| `.writerows(songs)` | writes every dict; `.writerow(one_dict)` writes just one |

> **Definition — `with` block:** a wrapper that opens a resource, runs the indented code, and closes the resource automatically at the end. Use it for every file you touch.

#### 🔍 Reading with `csv.DictReader`

```python
with open("songs.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    loaded = list(reader)         # turn the reader into a real list of dicts

print(len(loaded))                # 6
print(loaded[0])
```

Output:

```
6
{'title': 'Blue Lights', 'artist': 'Nova', 'genre': 'pop', 'minutes': '3.5', 'plays': '120'}
```

Look hard at the last two values: `'3.5'` and `'120'`. **With quotes.** They are strings now.

`DictReader` reads the header line and uses it as the keys automatically — that's the whole point of the "Dict" in the name. But it has no idea `plays` was ever a number.

#### ⚠️ The bug this causes

```python
print(songs[0]["plays"] + 10)      # 130   ← was an int
print(loaded[0]["plays"] + 10)     # 💥 TypeError
```

```
TypeError: can only concatenate str (not "int") to str
```

Exactly the `'5' + 5` error from Module 1, now arriving by post. And a sneakier version that does **not** crash:

```python
print(max(["120", "45", "300"]))   # '45'   ← WRONG, and silent
print(max([120, 45, 300]))         # 300    ← right
```

Why `'45'`? Strings compare **character by character**, like a dictionary. `'4'` comes after `'3'` and after `'1'`, so `'45'` wins. Your program reports the least-played song as the most-played and never says a word. This class of bug — *silently wrong, never crashes* — is the kind that gets into published results.

#### The fix: convert on load

You must state, in code, what type each column should be. Do it in a small typed loader:

```python
def load_songs(path):
    """Read the CSV and convert the numeric columns back to numbers."""
    records = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["minutes"] = float(row["minutes"])   # text → float
            row["plays"] = int(row["plays"])         # text → int
            records.append(row)
    return records

loaded = load_songs("songs.csv")
print(loaded[0])
print(loaded[0]["plays"] + 10)      # 130 ✔
```

Output:

```
{'title': 'Blue Lights', 'artist': 'Nova', 'genre': 'pop', 'minutes': 3.5, 'plays': 120}
130
```

> **Definition — round trip:** save data to a file, read it back, and check you got exactly what you started with. If the round trip fails, your saved file is not really your data.

Here's the whole journey in one picture:

```
   IN MEMORY                     ON DISK                     IN MEMORY AGAIN
 ┌───────────────┐            ┌────────────┐              ┌───────────────┐
 │ list of dicts │            │ songs.csv  │              │ list of dicts │
 │ plays: 120    │  ────────▶ │ ...,120    │  ─────────▶  │ plays: '120'  │
 │  (int)        │ DictWriter │  (text)    │  DictReader  │  (STRING! ⚠)  │
 └───────────────┘            └────────────┘              └───────┬───────┘
                                                                  │ int()
                                                                  ▼
                                                          ┌───────────────┐
                                                          │ plays: 120    │
                                                          │  (int) ✔      │
                                                          └───────────────┘
```

The `int()` step at the bottom is not optional. It is the whole job.

---

## 🔍 Worked Example

**The question:** *For the six songs, which genre has the most tracks, and what is the average play count of the pop songs?*

We'll trace every step with real numbers — no skipping.

### Step 0 — the data

| i | title | artist | genre | minutes | plays |
|---|---|---|---|---|---|
| 0 | Blue Lights | Nova | pop | 3.5 | 120 |
| 1 | Rain Check | Kabir | rock | 4.2 | 45 |
| 2 | Ghost Town | Nova | pop | 2.8 | 300 |
| 3 | Slow Train | Meera | folk | 5.1 | 60 |
| 4 | Neon Streets | Kabir | rock | 3.9 | 210 |
| 5 | Paper Boats | Nova | pop | 3.3 | 95 |

### Step 1 — trace `group_count(songs, "genre")` by hand

Start: `counts = {}`

| Turn | record | `value = r.get("genre")` | `counts.get(value, 0)` | after `counts[value] = ... + 1` |
|---|---|---|---|---|
| 1 | Blue Lights | `"pop"` | 0 (never seen) | `{'pop': 1}` |
| 2 | Rain Check | `"rock"` | 0 (never seen) | `{'pop': 1, 'rock': 1}` |
| 3 | Ghost Town | `"pop"` | 1 | `{'pop': 2, 'rock': 1}` |
| 4 | Slow Train | `"folk"` | 0 (never seen) | `{'pop': 2, 'rock': 1, 'folk': 1}` |
| 5 | Neon Streets | `"rock"` | 1 | `{'pop': 2, 'rock': 2, 'folk': 1}` |
| 6 | Paper Boats | `"pop"` | 2 | `{'pop': 3, 'rock': 2, 'folk': 1}` |

Final: `{'pop': 3, 'rock': 2, 'folk': 1}`

Sanity check by eye: pop appears on rows 0, 2, 5 → 3 ✔. rock on rows 1, 4 → 2 ✔. folk on row 3 → 1 ✔. Total 3 + 2 + 1 = 6 = number of rows ✔ (**always check the counts sum to `len(records)`** — if they don't, you dropped a row.)

**Answer to part 1: pop, with 3 tracks.**

### Step 2 — trace `filter_by(songs, "genre", "pop")`

| i | `r.get("genre")` | `== "pop"`? | kept? | `kept` so far |
|---|---|---|---|---|
| 0 | `"pop"` | True | ✅ | `[Blue Lights]` |
| 1 | `"rock"` | False | ❌ | `[Blue Lights]` |
| 2 | `"pop"` | True | ✅ | `[Blue Lights, Ghost Town]` |
| 3 | `"folk"` | False | ❌ | `[Blue Lights, Ghost Town]` |
| 4 | `"rock"` | False | ❌ | `[Blue Lights, Ghost Town]` |
| 5 | `"pop"` | True | ✅ | `[Blue Lights, Ghost Town, Paper Boats]` |

`len(pop) == 3` ✔ — and it matches the count from Step 1, which is a free cross-check.

### Step 3 — pull the `plays` column out of the filtered list

```python
pop = filter_by(songs, "genre", "pop")
pop_plays = [s["plays"] for s in pop]
```

`pop_plays` → `[120, 300, 95]`

### Step 4 — the arithmetic, shown in full

```
sum  = 120 + 300 + 95
     = 420 + 95
     = 515

count = 3

mean = 515 / 3
     = 171.666666...
     = 171.67   (rounded to 2 decimal places)
```

**Answer to part 2: the pop songs average 171.67 plays.**

### Step 5 — the same trace, as code that prints it

```python
def filter_by(records, key, value):
    return [r for r in records if r.get(key) == value]

def group_count(records, key):
    counts = {}
    for r in records:
        v = r.get(key, "MISSING")
        counts[v] = counts.get(v, 0) + 1
    return counts

counts = group_count(songs, "genre")
print("genre counts:", counts)
print("rows accounted for:", sum(counts.values()), "of", len(songs))

pop = filter_by(songs, "genre", "pop")
pop_plays = [s["plays"] for s in pop]
print("pop plays:", pop_plays)
print(f"pop average plays: {sum(pop_plays) / len(pop_plays):.2f}")
```

Output:

```
genre counts: {'pop': 3, 'rock': 2, 'folk': 1}
rows accounted for: 6 of 6
pop plays: [120, 300, 95]
pop average plays: 171.67
```

Every number matches the hand trace. That is what "checked" means.

### Step 6 — one honest caution

Three songs is a *tiny* sample. "Pop averages 171.67 plays" sounds like a fact about pop music; it is a fact about three songs, one of which (Ghost Town, 300) drags the average up hard. Drop it and the other two average 107.5. That's the mean-vs-median warning from Module 3 showing up in real data, and it is why Module 7 will teach you to *look* at a distribution before quoting an average from it.

---

## 💻 Hands-On

Create a folder called `module04/`. You'll write two files: `records.py` (the reusable tools) and `run_songs.py` (the program that uses them). Splitting tools from usage is the habit you started in Module 3.

### File 1 — `records.py`

```python
"""records.py — reusable tools for a dataset stored as a list of dictionaries.

Every function here works on ANY list of dicts, not just songs.
"""

import csv


def filter_by(records, key, value):
    """Return only the records whose `key` equals `value`.

    records : list of dicts
    key     : the column name to test, e.g. "genre"
    value   : the value to match, e.g. "pop"
    """
    kept = []                             # results go here
    for r in records:                     # visit every record once
        if r.get(key) == value:           # .get() -> None if key missing, never crashes
            kept.append(r)                # passed the test, keep this record
    return kept                           # RETURN, don't print (Module 3 rule)


def group_count(records, key):
    """Count records per distinct value of `key`. Returns a dict."""
    counts = {}                                   # empty set of buckets
    for r in records:
        v = r.get(key, "MISSING")                 # records lacking the key get their own bucket
        counts[v] = counts.get(v, 0) + 1          # add 1 to this bucket (0 if it's new)
    return counts


def group_sum(records, group_key, value_key):
    """Total up `value_key` for each distinct value of `group_key`."""
    totals = {}
    for r in records:
        g = r.get(group_key, "MISSING")           # which bucket
        totals[g] = totals.get(g, 0) + r.get(value_key, 0)   # add this row's number in
    return totals


def column(records, key):
    """Pull one column out as a plain list."""
    return [r.get(key) for r in records]          # list comprehension from Module 3


def save_csv(records, path, fieldnames):
    """Write records to a CSV file, columns in the order given by fieldnames."""
    with open(path, "w", newline="", encoding="utf-8") as f:   # newline="" is required
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()                      # the column-name line
        writer.writerows(records)                 # one line per record


def load_csv(path, converters=None):
    """Read a CSV back into a list of dicts.

    converters : optional dict like {"plays": int, "minutes": float}
                 telling us which columns to convert out of text.
    """
    if converters is None:                        # no conversions requested
        converters = {}                           # ...use an empty dict, not None
    records = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):             # each row arrives as a dict of STRINGS
            for key, convert in converters.items():
                if key in row:                    # only convert columns that exist
                    row[key] = convert(row[key])  # e.g. int("120") -> 120
            records.append(row)
    return records
```

### File 2 — `run_songs.py`

```python
"""run_songs.py — build a song dataset, interrogate it, save it, load it back."""

from records import (filter_by, group_count, group_sum,
                     column, save_csv, load_csv)      # import our own module

# ---------------------------------------------------------------- the dataset
songs = [
    {"title": "Blue Lights",  "artist": "Nova",  "genre": "pop",  "minutes": 3.5, "plays": 120},
    {"title": "Rain Check",   "artist": "Kabir", "genre": "rock", "minutes": 4.2, "plays": 45},
    {"title": "Ghost Town",   "artist": "Nova",  "genre": "pop",  "minutes": 2.8, "plays": 300},
    {"title": "Slow Train",   "artist": "Meera", "genre": "folk", "minutes": 5.1, "plays": 60},
    {"title": "Neon Streets", "artist": "Kabir", "genre": "rock", "minutes": 3.9, "plays": 210},
    {"title": "Paper Boats",  "artist": "Nova",  "genre": "pop",  "minutes": 3.3, "plays": 95},
]

FIELDS = ["title", "artist", "genre", "minutes", "plays"]   # fixed column order

# ------------------------------------------------------------------ inspect
print("=" * 46)
print(f"{len(songs)} records, {len(songs[0])} columns")
print("columns:", FIELDS)
print("=" * 46)

for s in songs:                                   # a quick printed table
    print(f"{s['title']:<14}{s['artist']:<8}{s['genre']:<6}"
          f"{s['minutes']:>5.1f}{s['plays']:>6}")

# ---------------------------------------------------------------- interrogate
print("\n-- counts by genre --")
for genre, n in group_count(songs, "genre").items():
    print(f"  {genre:<6}{n}")

print("\n-- total plays by artist --")
for artist, total in group_sum(songs, "artist", "plays").items():
    print(f"  {artist:<7}{total}")

pop = filter_by(songs, "genre", "pop")
pop_plays = column(pop, "plays")
print(f"\npop songs: {len(pop)}   plays: {pop_plays}")
print(f"pop average plays: {sum(pop_plays) / len(pop_plays):.2f}")

# a filter on a condition instead of an exact match: use a comprehension
long_songs = [s for s in songs if s["minutes"] > 3.6]
print("longer than 3.6 min:", column(long_songs, "title"))

# --------------------------------------------------------------- nested data
artists = {
    "Nova":  {"country": "India", "started": 2019, "members": ["Anya", "Rehan"]},
    "Kabir": {"country": "UK",    "started": 2016, "members": ["Kabir"]},
    "Meera": {"country": "India", "started": 2021, "members": ["Meera", "Dev", "Sana"]},
}

print("\n-- artist profiles --")
for name, info in artists.items():
    members = ", ".join(info["members"])          # join a list into one string
    print(f"  {name:<6}{info['country']:<7}since {info['started']}   [{members}]")

print("  Meera's country:", artists.get("Meera", {}).get("country", "unknown"))
print("  Zara's country :", artists.get("Zara", {}).get("country", "unknown"))

# ------------------------------------------------------------- the round trip
save_csv(songs, "songs.csv", FIELDS)
print("\nwrote songs.csv")

raw = load_csv("songs.csv")                       # NO converters on purpose
print("raw plays value:", repr(raw[0]["plays"]), "type:", type(raw[0]["plays"]).__name__)
print("raw max plays  :", max(column(raw, "plays")), "  <-- WRONG, text sorting")

typed = load_csv("songs.csv", converters={"minutes": float, "plays": int})
print("typed plays value:", repr(typed[0]["plays"]), "type:", type(typed[0]["plays"]).__name__)
print("typed max plays  :", max(column(typed, "plays")), " <-- right")

print("\nround trip identical?", typed == songs)
```

### Expected output

```
==============================================
6 records, 5 columns
columns: ['title', 'artist', 'genre', 'minutes', 'plays']
==============================================
Blue Lights   Nova    pop     3.5   120
Rain Check    Kabir   rock    4.2    45
Ghost Town    Nova    pop     2.8   300
Slow Train    Meera   folk    5.1    60
Neon Streets  Kabir   rock    3.9   210
Paper Boats   Nova    pop     3.3    95

-- counts by genre --
  pop   3
  rock  2
  folk  1

-- total plays by artist --
  Nova   515
  Kabir  255
  Meera  60

pop songs: 3   plays: [120, 300, 95]
pop average plays: 171.67
longer than 3.6 min: ['Rain Check', 'Slow Train', 'Neon Streets']

-- artist profiles --
  Nova  India  since 2019   [Anya, Rehan]
  Kabir UK     since 2016   [Kabir]
  Meera India  since 2021   [Meera, Dev, Sana]
  Meera's country: India
  Zara's country : unknown

wrote songs.csv
raw plays value: '120' type: str
raw max plays  : 95   <-- WRONG, text sorting
typed plays value: 120 type: int
typed max plays  : 300  <-- right

round trip identical? True
```

### Three things to notice

1. **`raw max plays` is 95, not 300.** The raw column is `['120','45','300','60','210','95']` — six *strings*. Python compares strings character by character, so it only ever looks at the first character unless there's a tie: `'9'` beats `'6'` beats `'4'` beats `'3'` beats `'2'` beats `'1'`. `'95'` wins. The song with the second-*lowest* play count is reported as the most-played, and nothing crashes.
2. **`round trip identical? True`** only happens because we converted `minutes` to `float` and `plays` to `int`. Delete the `converters=` argument and it prints `False`.
3. Open `songs.csv` in a spreadsheet. It looks like a normal table, because it is one.

> ✍️ **Build the habit:** before you run this file, write down on paper what you expect each of the last four lines to print. Then run it. The gap between your prediction and reality is the only part of programming that actually teaches you anything.

---

## ✍️ Practice

Work in `module04/`. Import from your `records.py` where it helps.

### 1. [Warm-up] Your profile card

Build a dictionary `me` with exactly these five keys: `name`, `age`, `city`, `favourite_subject`, `hours_of_sleep`. Then:

- print every pair using `.items()`, one per line, formatted as `key: value`
- print `me.get("pet", "no pet recorded")`
- add a new key `dream_job`, then print the dictionary's length before and after

**Done looks like:** seven printed lines, no `KeyError` anywhere, and lengths of 5 then 6.

### 2. [Warm-up] Count above a threshold

Write `count_above(records, key, threshold)` that returns how many records have a numeric value strictly greater than `threshold` under `key`. Records missing the key must be skipped, not crash.

Test it on the six songs: `count_above(songs, "plays", 100)` and `count_above(songs, "minutes", 4.0)`.

**Done looks like:** the function returns `3` and `2`, and adding `{"title": "Mystery"}` (no `plays` key) to the list does not change the `plays` answer or raise an error.

### 3. [Build] `average_of(records, key)`

Write `average_of(records, key)` that returns the mean of one numeric column, **ignoring** records where the key is missing. If no record has the key, return `None` rather than crashing on division by zero.

**Done looks like:** `average_of(songs, "plays")` returns `138.33...`, `average_of(songs, "minutes")` returns `3.8` (printed as `3.80` with `:.2f`), and `average_of(songs, "tempo")` returns `None`.

### 4. [Build] `group_average(records, group_key, value_key)`

Using `group_sum` and `group_count` as building blocks (do not rewrite the loop), write `group_average` that returns a dict mapping each group to the *mean* of `value_key` in that group. Print average plays per genre and per artist.

**Done looks like:** per genre you get `pop` ≈ 171.67, `rock` = 127.5, `folk` = 60.0, and you have checked `rock` by hand: (45 + 210) / 2.

### 5. [Stretch] Flatten nested data

Take the `artists` dict-of-dicts from the Hands-On. Write `flatten_profiles(profiles)` that turns it into a list of flat dicts with keys `artist`, `country`, `started`, `member_count`, `members` — where `members` is the list joined into one string with `"; "` between names. Then save the flat version to `artists.csv` and load it back with the right converters.

**Done looks like:** three rows in the CSV, `started` and `member_count` come back as `int`, and `loaded == flattened` prints `True`.

### 6. [Stretch] A schema-checked loader

Write `load_typed(path, schema)` where `schema` is a dict like `{"title": str, "minutes": float, "plays": int}`. It must:

- convert each column using its function from the schema
- **raise a clear error** (use `raise ValueError("...")` with a helpful message) if the CSV's header is missing any key the schema names, or has an extra column the schema doesn't mention
- return the list of typed dicts

Prove it works two ways: a successful round trip on `songs.csv` that equals the original, and a deliberate failure where you pass a schema missing `"genre"` and catch the `ValueError` with `try`/`except`, printing the message.

**Done looks like:** `load_typed("songs.csv", full_schema) == songs` is `True`, and the bad-schema run prints your own error message instead of a traceback.

---

## 🤔 Think Deeper

### 1. Your school wants one dictionary per student. Which keys should exist — and which must never?

*How to reason about it:* list the keys you'd want for something useful (say, spotting who needs extra help in maths). Now for each key ask three questions: **Who else can read this file once it exists? What happens to this student if the file leaks? Could the same decision be made without this key?** Notice that "religion", "family income", and "home address" are all *easy* to add and very hard to un-add. A key you never collect is a key that can never leak, and CSV files get emailed around constantly.

### 2. `.get(key, 0)` fills a missing number with zero. When is that a lie?

*How to reason about it:* try it on three different columns. Missing `plays` on a brand-new song — zero is probably honest. Missing `rainfall_mm` for a day the sensor was broken — zero says "it did not rain", which you do not know. Missing `test_score` for an absent student — zero says "they failed". Work out what each fill does to the *average*, and ask whether the fallback is a measurement or a guess dressed as one. Then think about what `None` would cost you instead: more code, but no invented facts.

### 3. If a group has one member, should you report its average at all?

*How to reason about it:* in the worked example, `folk` has exactly one song, so "folk averages 60 plays" is really "one folk song got 60 plays" wearing a statistician's hat. Decide on a minimum group size *before* you look at the results, and think about why deciding it afterwards is a problem. Then consider a real version: a school publishing average scores per class, where one class has 3 students and another has 30. What does a reader assume when they see two numbers side by side with no group sizes shown?

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `KeyError: 'genre'` when looping over records | One record was typed with a different key (`"Genre"`, `"gerne"`) or is missing it entirely | Use `r.get("genre", default)`, and add a startup check: `for r in records: assert set(r) == set(FIELDS)` |
| Numbers behave like text after loading a CSV — `max()` gives a nonsense answer with no error | `csv.DictReader` returns every field as `str`, always | Convert on load: `row["plays"] = int(row["plays"])`, or pass a `converters` dict as in `load_csv` |
| The first row of data disappears / becomes the header | Forgot `writer.writeheader()`, so `DictReader` used song 1 as the column names | Always call `.writeheader()` immediately after creating the `DictWriter` |
| Blank line between every row in the CSV (Windows) | Opened the file without `newline=""` | `open(path, "w", newline="", encoding="utf-8")` — every time, no exceptions |
| `counts[value] += 1` raises `KeyError` the first time | `+=` needs the key to already exist | Use `counts[value] = counts.get(value, 0) + 1` |
| `d["k"]` used inside an f-string with the same quote type: `f"{s["title"]}"` | Quote collision confuses Python's parser | Alternate them: `f"{s['title']}"` |
| Two records accidentally share the same title and you never notice | Lists happily hold duplicates | Check early: `titles = column(records, "title")`, then `len(titles) == len(set(titles))` |
| A nested dict silently becomes the text `"{'a': 1}"` in your CSV | CSV cells hold text only; Python stringifies whatever you give it | Flatten before saving — one column per piece of information |

---

## 🛠️ Mini-Project — Record Store

### Goal

Build a **30-record dataset in code**, interrogate it with your own reusable functions, save it to CSV, load it back, and *prove* the round trip is lossless.

Pick one theme and stick to it:

- **Songs** — `title`, `artist`, `genre`, `minutes`, `plays`
- **Students** — `name`, `grade`, `house`, `attendance_pct`, `favourite_subject`
- **Matches** — `team`, `opponent`, `venue`, `runs`, `won`

Whatever you pick, you need **exactly 5 keys**, of which **at least 2 are numeric** and **at least 1 is categorical** (a small set of repeating values, like genre or house — that's what you'll group by).

### Starter steps

**Step 1 — set up (15 min).**
Create `store.py`. At the top define `FIELDS` as a list of your 5 key names. Import your `records.py`.

**Step 2 — type the data (45 min).**
Write out 30 records as a list of dicts. Rules that make the rest of the project work:

- Every record has all 5 keys, spelled identically. Copy-paste the first record as a template.
- Your categorical column should have **3–5 distinct values**, each appearing at least 3 times.
- Your numbers must be plausible and *varied* — include a couple of extremes on purpose, because you'll want them later.
- One record should be a deliberate near-duplicate of another (same category, different name). You'll use it to test your duplicate check.

**Step 3 — a validator (15 min).**

```python
def validate(records, fields):
    """Raise a clear error if any record has the wrong keys."""
    for i, r in enumerate(records):
        if set(r.keys()) != set(fields):
            missing = set(fields) - set(r.keys())
            extra = set(r.keys()) - set(fields)
            raise ValueError(f"record {i} bad keys — missing {missing}, extra {extra}")
    return True
```

Run it before anything else. Fixing a typo now is a minute; finding it in your CSV is an hour.

**Step 4 — interrogate (30 min).** Print answers to at least five questions, each on a labelled line:

1. How many records per category? (`group_count`)
2. What's the total of your main number per category? (`group_sum`)
3. What's the *average* of that number per category? (`group_average` from Practice 4)
4. Which single record has the largest value of your main number?
5. How many records beat the overall average? (`count_above` from Practice 2)

**Step 5 — save and prove the round trip (30 min).**

```python
save_csv(records, "store.csv", FIELDS)
loaded = load_csv("store.csv", converters={"plays": int, "minutes": float})  # your columns

print("rows out:", len(records), " rows in:", len(loaded))
print("round trip identical?", loaded == records)

if loaded != records:                          # find the FIRST difference, don't guess
    for i, (a, b) in enumerate(zip(records, loaded)):
        if a != b:
            print("first mismatch at row", i)
            print("  original:", a)
            print("  loaded  :", b)
            break
```

**Step 6 — open the CSV in a spreadsheet (15 min).** Google Sheets, Excel, or Numbers. Check the header row is your 5 column names and that you have 31 lines total (1 header + 30 records). Take a screenshot.

### Success criteria checklist

- [ ] Exactly 30 records, each with exactly the same 5 keys — proven by `validate()` running without error
- [ ] At least 2 numeric columns and 1 categorical column with 3–5 repeating values
- [ ] `filter_by(records, key, value)` and `group_count(records, key)` written by you, taking the key as an argument (not hard-coded)
- [ ] Five questions printed with clear labels and correct answers
- [ ] One answer verified **by hand** on paper — write the arithmetic in a comment
- [ ] `store.csv` exists, has 31 lines, and opens as a clean table in a spreadsheet
- [ ] `loaded == records` prints `True`, and you can explain in one sentence why it would print `False` without the converters
- [ ] A `# WHOSE DATA IS THIS?` comment at the bottom: if these were real people, who could be hurt by this file leaking, and which of your 5 columns is the riskiest?

### 🚀 Level it up

Add a **two-condition filter**: `filter_where(records, conditions)` where `conditions` is a dict like `{"genre": "pop", "artist": "Nova"}`, and a record must match **all** pairs to be kept. Then extend it to `filter_range(records, key, low, high)` for numeric columns. Combine them to answer a question none of your single filters could: *"pop songs by Nova between 3 and 4 minutes long."*

Hint for the first one:

```python
def filter_where(records, conditions):
    kept = []
    for r in records:
        if all(r.get(k) == v for k, v in conditions.items()):
            kept.append(r)
    return kept
```

`all(...)` returns `True` only if every test inside is true — the `and` of Module 2, applied to a whole collection at once.

---

## 🔑 Key Takeaways

- A **dictionary** looks values up by *name* instead of position, which means one dict can describe one whole thing — a song, a student, a match.
- `d["k"]` crashes on a missing key; `d.get("k", default)` doesn't. Choose crashing when a hole means your data is broken, and a default when holes are expected.
- A **list of dictionaries with identical keys is a table**: one dict per row, keys as columns. This is the shape every dataset in this level takes.
- The counting-dictionary line `counts[v] = counts.get(v, 0) + 1` groups and counts anything, and its totals should always add up to `len(records)`.
- Functions that take the *key* as an argument (`filter_by(records, key, value)`) work on every dataset you'll ever build; functions with the key hard-coded work on exactly one.
- **CSV stores text and nothing but text.** `csv.DictReader` hands back strings, so you must convert numeric columns yourself — and the failure mode is often a silently wrong answer, not a crash.
- Prove your round trip with `loaded == original`. If that isn't `True`, your file is not your data.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| dictionary (`dict`) | A box of labelled slots — you get things out by name, not by counting | `{"name": "Ishaan", "runs": 103}` |
| key | The label on a slot | `"runs"` |
| value | What's stored in the slot | `103` |
| `KeyError` | Python's way of saying "there's no slot with that label" | `player["age"]` when there's no `age` key |
| `.get()` | Polite asking — returns a fallback instead of crashing | `player.get("age", 0)` → `0` |
| `.items()` | Hands you the key and the value together on each loop turn | `for k, v in d.items():` |
| record | One dictionary describing one thing = one row of a table | `{"title": "Ghost Town", ...}` |
| list of dicts | Many records in a list — a table you can loop over | `songs` (6 records, 5 keys each) |
| filter | Keep only the rows that pass a test | `filter_by(songs, "genre", "pop")` → 3 rows |
| group and count | Sort rows into buckets by one column and count each bucket | `{'pop': 3, 'rock': 2, 'folk': 1}` |
| counting dictionary | The `counts[v] = counts.get(v, 0) + 1` pattern | builds the buckets above |
| nested data | A container inside a container — needs two lookups | `artists["Nova"]["country"]` |
| CSV | A plain-text table: header line, then one line per row, commas between fields | `title,artist,genre` then `Blue Lights,Nova,pop` |
| `csv.DictWriter` | Writes a list of dicts out as CSV lines | `writer.writerows(songs)` |
| `csv.DictReader` | Reads CSV lines back as dicts — **all values are text** | `{'plays': '120'}` not `{'plays': 120}` |
| round trip | Save it, load it, check it's identical | `loaded == songs` → `True` |
| schema | A written-down statement of which columns exist and what type each is | `{"plays": int, "minutes": float}` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Your profile card

```python
me = {
    "name": "Ramya",
    "age": 13,
    "city": "Bengaluru",
    "favourite_subject": "physics",
    "hours_of_sleep": 7.5,
}

print("length before:", len(me))          # 5

for key, value in me.items():             # .items() gives both at once
    print(f"{key}: {value}")

print(me.get("pet", "no pet recorded"))   # key missing -> our fallback, no crash

me["dream_job"] = "engineer"              # assigning to a NEW key adds it
print("length after:", len(me))           # 6
```

Output:

```
length before: 5
name: Ramya
age: 13
city: Bengaluru
favourite_subject: physics
hours_of_sleep: 7.5
no pet recorded
length after: 6
```

**Why it works:** assignment to an existing key replaces; assignment to a new key appends. `.get("pet", ...)` never raises `KeyError` because the second argument is what it returns when the key is absent.

---

### 2. [Warm-up] Count above a threshold

```python
def count_above(records, key, threshold):
    """How many records have records[key] > threshold? Missing keys are skipped."""
    n = 0
    for r in records:
        v = r.get(key)                   # None if the key isn't there
        if v is None:                    # skip, don't crash, don't count
            continue
        if v > threshold:
            n += 1
    return n


print(count_above(songs, "plays", 100))     # 3
print(count_above(songs, "minutes", 4.0))   # 2

songs_plus = songs + [{"title": "Mystery"}]   # a record with only one key
print(count_above(songs_plus, "plays", 100))  # still 3, no error
```

**Hand check — `plays > 100`:** 120 ✔, 45 ✘, 300 ✔, 60 ✘, 210 ✔, 95 ✘ → **3**.
**Hand check — `minutes > 4.0`:** 3.5 ✘, 4.2 ✔, 2.8 ✘, 5.1 ✔, 3.9 ✘, 3.3 ✘ → **2**.

**Why `if v is None` and not `if not v`:** `not v` is also `True` when `v` is `0`, so a genuine zero would get skipped as if it were missing. `is None` asks the exact question you mean. This distinction bites people constantly — remember it.

---

### 3. [Build] `average_of(records, key)`

```python
def average_of(records, key):
    """Mean of one numeric column, skipping records that lack the key.
    Returns None if no record has it."""
    values = []
    for r in records:
        v = r.get(key)
        if v is not None:
            values.append(v)
    if len(values) == 0:                 # guard against ZeroDivisionError
        return None
    return sum(values) / len(values)


print(average_of(songs, "plays"))      # 138.33333333333334
print(average_of(songs, "minutes"))    # 3.8000000000000003   <-- see the float note below
print(average_of(songs, "tempo"))      # None
print(f"{average_of(songs, 'plays'):.2f}")   # 138.33
```

**Hand check — plays:**

```
120 + 45 = 165
165 + 300 = 465
465 + 60 = 525
525 + 210 = 735
735 + 95 = 830
830 / 6 = 138.3333...
```

**Hand check — minutes:**

```
3.5 + 4.2 = 7.7
7.7 + 2.8 = 10.5
10.5 + 5.1 = 15.6
15.6 + 3.9 = 19.5
19.5 + 3.3 = 22.8
22.8 / 6 = 3.8
```

> Floating-point note: `22.8 / 6` is exactly `3.8` on paper, but Python prints `3.8000000000000003`. That's the float rounding you met in Module 1 — the decimals 3.5, 4.2, 2.8… can't be stored perfectly in binary, so the sum is a hair off. Your code is fine. Format with `:.2f` whenever you *display* a float: `f"{average_of(songs, 'minutes'):.2f}"` → `3.80`.

---

### 4. [Build] `group_average(records, group_key, value_key)`

```python
def group_average(records, group_key, value_key):
    """Mean of value_key within each group, built from the two tools we already have."""
    totals = group_sum(records, group_key, value_key)     # {'pop': 515, 'rock': 255, 'folk': 60}
    counts = group_count(records, group_key)              # {'pop': 3,   'rock': 2,   'folk': 1}
    averages = {}
    for g in totals:                                      # same keys in both dicts
        averages[g] = totals[g] / counts[g]
    return averages


print("avg plays per genre:")
for g, a in group_average(songs, "genre", "plays").items():
    print(f"  {g:<6}{a:.2f}")

print("avg plays per artist:")
for a_name, a_val in group_average(songs, "artist", "plays").items():
    print(f"  {a_name:<7}{a_val:.2f}")
```

Output:

```
avg plays per genre:
  pop   171.67
  rock  127.50
  folk  60.00
avg plays per artist:
  Nova   171.67
  Kabir  127.50
  Meera  60.00
```

**Hand check — rock:** Rain Check 45 + Neon Streets 210 = 255. 255 / 2 = **127.5** ✔
**Hand check — folk:** one song, 60. 60 / 1 = **60.0** ✔

**Interesting coincidence:** the genre and artist averages match exactly. That's because in this tiny dataset each artist happens to sit in exactly one genre — Nova is all pop, Kabir all rock, Meera all folk. Spotting that two columns carry the *same information* is a real data-analysis skill; you'll meet it again in Module 6 as a reason to drop a redundant column.

**Why reuse instead of rewriting:** if you later fix a bug in `group_count` (say, how it handles missing keys), `group_average` inherits the fix for free. That's the Module 3 argument for functions, one level up.

---

### 5. [Stretch] Flatten nested data

```python
import csv
from records import save_csv, load_csv

artists = {
    "Nova":  {"country": "India", "started": 2019, "members": ["Anya", "Rehan"]},
    "Kabir": {"country": "UK",    "started": 2016, "members": ["Kabir"]},
    "Meera": {"country": "India", "started": 2021, "members": ["Meera", "Dev", "Sana"]},
}


def flatten_profiles(profiles):
    """dict-of-dicts  ->  list of flat dicts that CSV can actually store."""
    rows = []
    for name, info in profiles.items():          # name is the outer key
        rows.append({
            "artist": name,                      # promote the outer key to a column
            "country": info["country"],
            "started": info["started"],
            "member_count": len(info["members"]),
            "members": "; ".join(info["members"]),   # list -> one text field
        })
    return rows


FLAT_FIELDS = ["artist", "country", "started", "member_count", "members"]

flattened = flatten_profiles(artists)
for row in flattened:
    print(row)

save_csv(flattened, "artists.csv", FLAT_FIELDS)

loaded = load_csv("artists.csv", converters={"started": int, "member_count": int})
print("round trip identical?", loaded == flattened)
```

Output:

```
{'artist': 'Nova', 'country': 'India', 'started': 2019, 'member_count': 2, 'members': 'Anya; Rehan'}
{'artist': 'Kabir', 'country': 'UK', 'started': 2016, 'member_count': 1, 'members': 'Kabir'}
{'artist': 'Meera', 'country': 'India', 'started': 2021, 'member_count': 3, 'members': 'Meera; Dev; Sana'}
round trip identical? True
```

The file `artists.csv` contains:

```
artist,country,started,member_count,members
Nova,India,2019,2,Anya; Rehan
Kabir,UK,2016,1,Kabir
Meera,India,2021,3,Meera; Dev; Sana
```

**Two design decisions worth naming:**

1. **`"; "` not `", "`.** A comma inside a field forces the CSV writer to wrap the whole field in quotes, which still works but is harder to read and easy to break by hand-editing. A semicolon sidesteps it entirely.
2. **`member_count` is stored, not recomputed.** It's redundant — you could always split `members` and count. Storing it means you can group and sort by it without any parsing. Redundancy costs a little space and buys a lot of convenience; the risk is that the two columns can drift apart if someone edits one and not the other.

**To get the list back on load** you'd add a converter of your own:

```python
loaded2 = load_csv("artists.csv", converters={
    "started": int,
    "member_count": int,
    "members": lambda s: s.split("; "),      # text -> list again
})
print(loaded2[0]["members"])                 # ['Anya', 'Rehan']
```

---

### 6. [Stretch] A schema-checked loader

```python
import csv


def load_typed(path, schema):
    """Read a CSV, checking the header against `schema` and converting every column.

    schema : dict of column_name -> conversion function, e.g. {"plays": int}
    Raises ValueError if the header and the schema don't name exactly the same columns.
    """
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames                  # list of column names, or None on empty file

        if header is None:
            raise ValueError(f"{path} is empty — no header row found")

        missing = set(schema) - set(header)         # schema wants it, file doesn't have it
        extra = set(header) - set(schema)           # file has it, schema never mentioned it
        if missing or extra:
            raise ValueError(
                f"schema does not match {path}: "
                f"missing from file {sorted(missing)}, "
                f"unexpected in file {sorted(extra)}"
            )

        records = []
        for line_no, row in enumerate(reader, start=2):     # line 1 was the header
            typed = {}
            for name, convert in schema.items():
                raw = row[name]
                try:
                    typed[name] = convert(raw)
                except ValueError:
                    raise ValueError(
                        f"line {line_no}: cannot convert column '{name}' "
                        f"value {raw!r} using {convert.__name__}"
                    )
            records.append(typed)

    return records
```

**Proof 1 — the good schema round-trips:**

```python
FULL_SCHEMA = {
    "title": str,
    "artist": str,
    "genre": str,
    "minutes": float,
    "plays": int,
}

save_csv(songs, "songs.csv", list(FULL_SCHEMA.keys()))
back = load_typed("songs.csv", FULL_SCHEMA)
print("round trip identical?", back == songs)
print(back[0])
```

```
round trip identical? True
{'title': 'Blue Lights', 'artist': 'Nova', 'genre': 'pop', 'minutes': 3.5, 'plays': 120}
```

It's `True` because we wrote the columns in schema order and `dict` equality in Python **ignores key order** — `{"a": 1, "b": 2} == {"b": 2, "a": 1}` is `True`. Order matters for the *file*, not for the comparison.

**Proof 2 — the bad schema is caught:**

```python
BAD_SCHEMA = {"title": str, "artist": str, "minutes": float, "plays": int}   # no "genre"

try:
    load_typed("songs.csv", BAD_SCHEMA)
except ValueError as e:
    print("caught:", e)
```

```
caught: schema does not match songs.csv: missing from file [], unexpected in file ['genre']
```

Read the message carefully: nothing is missing *from the file* — the file has everything the schema asked for. What's wrong is the file has a column (`genre`) the schema never mentioned, so loading would silently drop it. Silently dropping a column is exactly the kind of thing that ruins an analysis three weeks later, which is why this loader refuses.

**Proof 3 (bonus) — a bad value is caught with its line number:**

Hand-edit `songs.csv` so one `plays` value reads `many`, then:

```
caught: line 3: cannot convert column 'plays' value 'many' using int
```

**Why `str` is in the schema for text columns:** `str("Nova")` is just `"Nova"`, so it does nothing to the value. But listing it means the schema is a *complete* statement of the table's shape, and the missing/extra check can do its job. A schema that only names some columns can't tell you when a column appears out of nowhere.

**Why `{convert.__name__}` works:** every Python function knows its own name. `int.__name__` is `'int'`, `float.__name__` is `'float'`. Small trick, much better error messages.

</details>

---

[⬅ Previous](module-03-functions-and-lists.md) · [Level 2 Home](README.md) · [Next ➡](module-05-numpy-arrays.md)

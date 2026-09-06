# Module 1 — What AI Is, What It Isn't, and Where It's Hiding in Your Day

**Level 1 · Module 1 · ~2.5 hours · Prereqs: none — you need a pencil, paper, and a phone or computer you already use**

[⬅ Previous](../../CURRICULUM_MAP.md) · [Level 1 Home](README.md) · [Next ➡](module-02-data-is-everywhere.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** define artificial intelligence in one plain sentence — without using the words "smart" or "brain".
2. **You will be able to** sort any system you meet into one of three families: **rule-following**, **learned-from-examples**, or **generating-new-content**.
3. **You will be able to** name five AI systems you personally touched in the last 24 hours and say exactly what each one is guessing.
4. **You will be able to** explain one thing today's AI genuinely cannot do — and why that fact surprises most adults.
5. **You will be able to** argue a hard case (a system that could go in two boxes) and defend your call with a reason, not a feeling.

---

## 🪝 The Hook

In 2016, a computer program called AlphaGo beat the world's best human player at Go, a board game so complicated that there are more possible games than atoms in the observable universe. Newspapers everywhere printed the same headline: *machines are thinking now.*

Here is the part they did not print. That same program could not play checkers. It could not tell you what a Go board is made of. If you had asked it "are you tired?" it would have replied with a Go move, because a Go move is the only thing it can produce. It had one skill, and outside of that one skill it was completely blank.

So which is it — a thinking machine, or a very fancy calculator?

That question is the whole module. By the end you will have a test you can run on any system in about thirty seconds, and you will never again have to guess whether something is "real AI".

---

## 🧠 The Concept

We're going to build your understanding in five steps. Each step gives you one new word, one everyday anchor, and one tiny example with real numbers.

---

### 1️⃣ Artificial intelligence: a machine doing a job that used to need a person's judgement

Imagine your school's front desk. A visitor walks in. Someone has to decide: *is this person allowed inside?* That decision needs **judgement** — looking, weighing, and choosing. For a hundred years, only a human could do it.

Now imagine a camera at the gate that reads number plates and lifts the barrier for cars on the approved list. A job that needed a person's judgement is now done by a machine.

> **Artificial intelligence (AI)** — getting a machine to do a job that used to need a person's judgement.

Read that definition again. Notice what is *not* in it:

- It does not say "smart".
- It does not say "brain".
- It does not say "thinks", "understands", "wants", or "feels".
- It does not say the machine has to do the job the same way a person would.

That last point matters more than anything else in this module. A submarine does not swim like a fish. It moves through water using a completely different method, and it still gets from one port to another. AI systems do jobs that needed judgement, using methods that are nothing like human thinking.

**🍕 Analogy — the pizza-cutter test.**
A pizza cutter does a job (slicing) that a person used to do with a knife. Is a pizza cutter AI? No — because slicing is not *judgement*. It's a physical action with no decision in it. But "look at this pizza and decide whether it's burnt enough to throw away" — that's judgement. If a machine did *that*, it would be AI.

The word to circle in the definition is **judgement**: a choice where reasonable people could disagree, and where the answer depends on looking at the specific case.

**🔢 Tiny example.**
Here are five jobs. Which need judgement?

| Job | Needs judgement? | Why |
|---|---|---|
| Add 47 + 88 | ❌ No | One exact answer, one exact method |
| Decide if a photo shows a dog or a wolf | ✅ Yes | Depends on the specific photo; people can disagree |
| Ring a bell at 3:30 pm every day | ❌ No | A clock does it; no case-by-case choice |
| Decide which YouTube video to show you next | ✅ Yes | Depends on you, right now |
| Sort 200 numbers from smallest to largest | ❌ No | One exact answer, one exact method |

Two of five need judgement. Only those two are candidates for AI.

---

### 2️⃣ Rule-based systems: a human writes the if-then steps

The oldest way to get a machine to make a decision is to have a human write down every step, in advance, in the form **if this, then that**.

> **Rule-based system** — a system where a human wrote the decision steps by hand, as if-then instructions, before the machine ever ran.

**🍕 Analogy — your mum's note on the fridge.**
"If the milk smells bad, throw it out. If the bread has green spots, throw it out. Otherwise, it's fine for breakfast."

That note is a rule-based system for food safety. A human (your mum) thought about it in advance and wrote down the steps. The note does not learn. If a new food goes bad in a new way, the note is silent until someone edits it.

**Real machines that work this way:**

- A **thermostat**: `IF room_temperature < 20°C THEN turn_on_heater`
- An **old spell-checker**: it holds a list of 100,000 correct words. `IF the word is not in the list THEN underline it in red.`
- A **traffic light** on a timer: `IF 30 seconds have passed THEN switch to amber`
- A **vending machine**: `IF coins_inserted >= price THEN release item AND return change`

**🔢 Tiny example — a spell-check word list.**

Suppose the dictionary contains: `cat, cot, cut, dog, dot`.

You type: `dat`

The system checks: is `dat` in the list? Look at all five entries — no match. So it underlines `dat` in red.

Now you type: `dot`. Is `dot` in the list? Yes, it's the fifth entry. So no red underline.

Now here's the crack in the system. You type: **`I have a pet dot.`**

You meant `dog`. The system sees `dot`, finds it in the list, and stays silent. It cannot catch your mistake because nobody wrote a rule about pets and dots. The rules only know what a human put in them.

**Key property:** a rule-based system is *predictable* and *explainable*. You can always point at the exact line that caused the answer. That is a real advantage — and Module 3 will show you where it falls apart.

---

### 3️⃣ Machine learning: the machine finds the rule itself, from examples

Now flip it around. Instead of a human writing the rule, the human gathers **examples with answers attached**, and the machine works out the rule on its own.

> **Machine learning (ML)** — the machine finds the decision rule itself by studying many examples where someone already wrote down the correct answer.

**🍕 Analogy — learning to spot a ripe mango.**
Nobody ever gave you an if-then list for ripe mangoes. You did not memorise "IF the colour value is between orange-42 and orange-58 AND the softness index is 3, THEN ripe." Instead, over years, you saw hundreds of mangoes and someone said "that one's ripe" or "not yet". You absorbed the pattern. Now you can pick a ripe mango you have never seen before, and you cannot fully explain how.

Machine learning is that, done by a machine, in minutes instead of years.

**🔢 Tiny example — learning "spam or not" from 6 messages.**

A human collects six text messages and writes the correct answer next to each:

| # | Message | Correct answer |
|---|---|---|
| 1 | "WIN a FREE phone now!!!" | spam |
| 2 | "Are you coming to practice?" | not spam |
| 3 | "FREE money click here!!!" | spam |
| 4 | "Mum said dinner at 7" | not spam |
| 5 | "Claim your FREE prize!!!" | spam |
| 6 | "Did you finish the maths?" | not spam |

Nobody tells the machine what to look for. The machine counts things. It notices:

- The word **FREE** appears in 3 of 3 spam messages and 0 of 3 not-spam messages.
- **Exclamation marks (!!!)** appear in 3 of 3 spam and 0 of 3 not-spam.
- The word **you** appears in 1 spam and 2 not-spam — not a useful clue.

From counting alone, the machine builds a guessing rule roughly like: *messages containing FREE and multiple exclamation marks are probably spam.* No human wrote that. The machine extracted it from the six examples.

That extracted guessing rule has a name:

> **Model** — the guessing machine that comes out of the learning process. Give it a new input, it gives you a guess.

The whole pipeline in one picture:

```
   ┌────────────────────────────────────────────────────────┐
   │  RULE-BASED SYSTEM                                     │
   │                                                        │
   │   Human thinks  ──►  writes IF-THEN rules  ──► MACHINE │
   │                                                 │      │
   │                        new input  ─────────────►│      │
   │                                                 ▼      │
   │                                              answer    │
   └────────────────────────────────────────────────────────┘

   ┌────────────────────────────────────────────────────────┐
   │  MACHINE LEARNING                                      │
   │                                                        │
   │   Human collects EXAMPLES + correct ANSWERS            │
   │                    │                                   │
   │                    ▼                                   │
   │            ┌───────────────┐                           │
   │            │   TRAINING    │  (machine finds the rule) │
   │            └───────┬───────┘                           │
   │                    ▼                                   │
   │            ┌───────────────┐                           │
   │            │     MODEL     │  ◄──── new input          │
   │            └───────┬───────┘                           │
   │                    ▼                                   │
   │                 answer                                 │
   └────────────────────────────────────────────────────────┘
```

**Key property:** a machine-learning system is *not fully explainable*. Nobody can point at line 47 and say "that's why". It can also be wrong in surprising ways — because it learned from whatever examples it was given, including their mistakes.

---

### 4️⃣ Generative AI: systems that produce new content, not just labels

The spam system above produces one of two words: `spam` or `not spam`. It picks from a short list. That's a **label**.

> **Label** — the answer a system produces when it chooses from a fixed set of options.

But some systems don't pick from a list. They *build* something that never existed before, piece by piece.

> **Generative AI** — a system that produces new content (text, images, sound, video) instead of choosing a label from a list.

**🍕 Analogy — the multiple-choice test vs the essay.**
A multiple-choice question gives you four boxes and you tick one. That's labelling. An essay question gives you a blank page and you write 300 words that have never been written in that order before. That's generating.

Same student, same brain, two completely different kinds of output. Same idea with AI.

**🔢 Tiny example — how many possible answers?**

| System | Its possible outputs | How many? |
|---|---|---|
| Spam filter | `spam`, `not spam` | 2 |
| Photo animal classifier | `cat`, `dog`, `bird`, `horse`, `fish` | 5 |
| Handwriting digit reader | `0`–`9` | 10 |
| Chatbot writing a paragraph | any sequence of words | effectively unlimited |
| Image generator | any picture | effectively unlimited |

The line is clear: **a small fixed menu = labelling. An unlimited blank page = generating.**

Generative systems are still machine learning underneath — they learned from examples too. Generative AI is a *kind* of machine learning, not a separate thing. Think of it like this:

```
        ┌──────────────────────────────────────────────┐
        │        ARTIFICIAL INTELLIGENCE               │
        │                                              │
        │  ┌────────────────┐   ┌───────────────────┐  │
        │  │  RULE-BASED    │   │ MACHINE LEARNING  │  │
        │  │                │   │                   │  │
        │  │ human writes   │   │ ┌───────────────┐ │  │
        │  │ the if-then    │   │ │ GENERATIVE AI │ │  │
        │  │ steps          │   │ │ makes new     │ │  │
        │  │                │   │ │ content       │ │  │
        │  │ thermostat     │   │ └───────────────┘ │  │
        │  │ spell list     │   │                   │  │
        │  │ vending machine│   │ spam filter       │  │
        │  │                │   │ face unlock       │  │
        │  │                │   │ recommendations   │  │
        │  └────────────────┘   └───────────────────┘  │
        └──────────────────────────────────────────────┘
```

Generative AI sits *inside* machine learning. When you sort a system, ask two questions in order:

1. Did a human write the rules, or did the machine learn them from examples?
2. If it learned — does it output a label from a menu, or new content from a blank page?

---

### 5️⃣ Narrow vs general: why every real system today is narrow

Here's the thing the movies get wrong.

> **Narrow AI** — a system that can do exactly one job, and is completely blank outside it.
>
> **General AI (AGI)** — a hypothetical system that could learn and do *any* job a person can, switching between them the way you do. It does not exist.

**🍕 Analogy — the world's greatest samosa chef.**
Imagine a chef who makes the finest samosa on Earth. Crispier than yours, better than mine, perfect every time. Now ask her to fix a bicycle. She cannot. Ask her to teach algebra. She cannot. Ask her to make a pizza — a food, like samosas, made of dough — and she cannot, because she only ever learned samosas.

Every real AI system today is that chef. Superb at one thing. Blank at everything else.

**🔢 Tiny example — the counting test.**

| System | Number of jobs it can do |
|---|---|
| AlphaGo | 1 (play Go) |
| Your phone's face unlock | 1 (is this the owner's face?) |
| A spam filter | 1 (spam or not) |
| Google Translate | 1 (turn text in language A into language B) |
| A modern chatbot | Looks like many — but it is 1: predict the next chunk of text |
| **You** | Effectively unlimited |

That last row is why "narrow" matters. You are reading this, and you could stop and make toast, comfort a friend, learn to juggle, and argue about a football match. No machine can do that set.

Even a chatbot that appears to do a hundred jobs is doing one job — *guess what text comes next* — over and over. Module 8 will show you exactly how that works, with tally marks and no magic.

**⚠️ The thing today's AI genuinely cannot do — and why it surprises people.**

Today's AI cannot **reliably know when it doesn't know**.

A person who has never seen a Pomeranian will say "I'm not sure what that is." A model trained on cats and dogs, shown a Pomeranian, will confidently say "dog — 94%". Shown a *chair*, it will still say "dog — 71%", because "chair" is not on its menu. It has no option for "that's outside my world".

This surprises people because the confident tone reads like understanding. It is not. It is a number coming out of a machine that was only ever built to pick from a menu. Module 5 will let you feel this yourself, and Module 9 will show you why it's dangerous.

---

## 🔍 Worked Example

Let's take one system all the way through the sorting test, step by step, showing every decision.

**The system: your phone's Photos app finding all your pictures of your dog.**

---

**Step 1 — What goes in? What comes out?**

| | |
|---|---|
| **Input** | One photo (a grid of colour dots) |
| **Output** | A list of tags for that photo, e.g. `dog`, `outdoors`, `grass` |

Write these down first, always. If you cannot name the input and the output, you do not understand the system yet.

---

**Step 2 — Does this job need judgement?**

Two people look at a blurry photo taken at dusk. One says "that's a dog." The other says "that's a fox." They disagree, and both are being reasonable. Disagreement between reasonable people is the signature of judgement.

✅ **Yes, judgement.** So this is a candidate for AI.

---

**Step 3 — Could a human have written if-then rules for it?**

Let's actually try. Write a rule that catches dogs.

- Attempt 1: `IF the photo contains a four-legged animal THEN dog.` — Fails on cats, horses, goats, and tables.
- Attempt 2: `IF the photo contains a four-legged animal AND it has floppy ears THEN dog.` — Fails on rabbits (floppy ears), and misses German Shepherds (pointy ears).
- Attempt 3: add `OR pointy ears` — now it catches cats again.

And every attempt has a deeper problem: the rule mentions "ears", but the machine only receives numbers describing colour dots. There is no `ears` input to test. A human would have to write a rule that finds ears in a grid of millions of numbers — for every possible angle, lighting, and dog.

❌ **No, a human could not write these rules.** That is a very strong signal.

---

**Step 4 — Where did the decision rule come from?**

The company trained the tagger on millions of photos that people had already labelled. It counted patterns across those photos until it could predict labels on new ones.

✅ **Machine learning.**

---

**Step 5 — Label or new content?**

Its output menu is a fixed list of tags: `dog`, `cat`, `beach`, `food`, `birthday`, and so on. Perhaps 1,000 options. It never invents a new tag, and it never draws you a new picture.

✅ **Label.** So this is machine learning, but *not* generative AI.

---

**Step 6 — Narrow or general?**

It tags photos. Show it a maths problem and it will tag it `document` or `whiteboard`. It has no ability to solve the problem.

✅ **Narrow.**

---

**Final verdict, written out the way you'll write it in the mini-project:**

> **Photos app auto-tagging.** Input: one photo. Output: tags from a fixed list. Family: **machine learning (non-generative)**. Reason: no human could write if-then rules over raw colour dots for every dog on Earth, and the company trained it on millions of already-labelled photos. Narrow: it only tags images.

---

**Now a hard case, traced the same way — a car's cruise control.**

| Step | Finding |
|---|---|
| Input | Current speed, target speed |
| Output | Amount of accelerator to apply |
| Judgement? | Borderline — but no. Any two engineers would compute the same answer. There is one correct amount. |
| Rules writable? | Yes: `IF current_speed < target THEN increase throttle` |
| Where did the rule come from? | An engineer wrote it |
| Verdict | **Rule-based — and arguably not AI at all**, because holding a speed is not judgement, it's measurement plus arithmetic |

Compare that to **adaptive cruise control**, which watches the car ahead through a camera and slows down for it. That system must first answer "is there a car ahead, and how far?" from camera images — which is exactly the dog-tagging problem again. That part **is** machine learning.

Same product name, one word different, two different families. This is why you trace the input and the output *first*.

---

## 💻 Hands-On

**Level 1 uses no programming languages.** Everything here runs in a browser or on paper. Set aside about 40 minutes.

---

### Activity A — Play against a learned model (Quick, Draw!) — 15 min

1. Open a browser and go to **`quickdraw.withgoogle.com`**.
2. Click **Let's Draw!**
3. You'll be asked to draw six things in 20 seconds each. Draw them.
4. Watch the bottom of the screen while you draw — the system calls out its guesses out loud as your lines appear.

**What to write down while you play** (copy this table onto paper):

| Round | What you were asked to draw | Guesses it called out, in order | Did it get it? | Seconds it took |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |

**Expected experience:** on simple, common shapes (clock, sun, ladder) it usually guesses within 2–4 seconds and often names two or three wrong things first — "is it a wheel? is it a donut? … it's a clock!" On unusual prompts (kangaroo, harp, camouflage) it often fails entirely even when your drawing is good.

**Now the important part.** After you finish, the site shows you what other people drew for the same prompt. Click one of your prompts and look at 20 of those drawings.

Answer in writing:

- Did most people draw it the same way? (For "clock" — almost everyone draws a circle with two hands. For "camouflage" — everyone draws something different.)
- Prompts where everyone draws the same thing are the ones the model gets right. Why do you think that is?

You just discovered, from evidence, that **a learned model is only as good as the examples it saw**. Hold onto that. It is Module 5's entire lesson.

---

### Activity B — Build a rule-based system on paper, then break it — 15 min

You are going to *be* a rule-based system. No learning allowed.

**The job:** decide if a word is a real English word.

**Your rulebook** — you may use exactly these five rules, in this order:

```
RULE 1: IF the word has no vowels (a, e, i, o, u)  THEN not-a-word
RULE 2: IF the word has 4 or more of the same letter in a row  THEN not-a-word
RULE 3: IF the word starts with "zq", "xj", or "vk"  THEN not-a-word
RULE 4: IF the word is longer than 20 letters  THEN not-a-word
RULE 5: OTHERWISE  THEN it-is-a-word
```

Apply the rules **strictly and in order** to these ten words. Stop at the first rule that fires. Fill in the table:

| Word | First rule that fires | Verdict | Actually a real word? | Correct? |
|---|---|---|---|---|
| `banana` | | | yes | |
| `zqrtle` | | | no | |
| `rhythm` | | | yes | |
| `flumbergast` | | | no | |
| `aaaargh` | | | no | |
| `strengths` | | | yes | |
| `xjmp` | | | no | |
| `crypt` | | | yes | |
| `hello` | | | yes | |
| `qwrtplk` | | | no | |

**Expected result:** the rulebook gets 7 of 10 correct. It fails on `rhythm` and `crypt` (Rule 1 wrongly rejects them — no a/e/i/o/u) and on `flumbergast` (Rule 5 wrongly accepts it — it looks perfectly word-shaped but isn't real).

**Then answer:** Add a 6th rule that fixes `rhythm` and `crypt`. Now try to add a 7th rule that fixes `flumbergast` *without* breaking `banana` and `hello`. Spend 3 minutes genuinely trying.

You will not succeed. There is no shape-based rule that separates `flumbergast` from `banana` — they are both pronounceable, both vowel-balanced, both ordinary-looking. The only thing that separates them is *a human once decided one is a word and the other is not*, which is a fact about the world, not a pattern in the letters.

**That is the wall.** Module 3 is entirely about that wall.

---

### Activity C — Talk to a generative system and catch it inventing — 10 min

Use any chatbot an adult has approved for you (Claude, ChatGPT, Gemini, or a school-provided one). **Have an adult present.**

Type exactly this:

```
Tell me about the 1987 Australian film "The Glass Kangaroo of Wollongong",
including its director and how it was received.
```

**That film does not exist.** It is invented. Watch what happens.

**Expected output:** many chatbots will produce a fluent, confident paragraph with a made-up director, a made-up plot, and a made-up review — because their one job is to produce text that *sounds like* the right kind of text. Some newer or more careful ones will say "I can't find a record of that film." Both outcomes teach you something.

Record:

| Question | Your answer |
|---|---|
| Did it invent details? | |
| How confident did it sound, 1–5? | |
| Did it warn you at all? | |
| Would you have believed it if you didn't already know? | |

Now try this follow-up:

```
Was that film real? Answer with just yes or no.
```

Note whether it changes its story. A system that confidently makes something up and then reverses when challenged is showing you exactly what it is: a text-shaped-output machine, not a knowledge machine.

> ⚠️ **Ground rule for the rest of this course:** a chatbot's confidence tells you nothing about whether it is right. Confidence and correctness are two separate things. Write that on a sticky note.

---

## ✍️ Practice

**[Warm-up] 1 — The one-sentence definition.**
Write a definition of artificial intelligence in **one sentence**, in your own words. Banned words: *smart, brain, think, intelligent, robot, conscious, magic.*
*Done looks like:* one sentence, under 25 words, using none of the banned words, and it would still make sense read aloud to a 7-year-old.

**[Warm-up] 2 — Sort the eight.**
Copy this table and fill in the last two columns. For family, write exactly one of: `rule-based`, `machine learning`, `generative AI`, or `not AI`.

| System | Input | Output | Family | One-line reason |
|---|---|---|---|---|
| Calculator app | | | | |
| Phone face unlock | | | | |
| Microwave timer | | | | |
| Netflix "because you watched…" row | | | | |
| Chatbot writing a poem | | | | |
| Automatic doors at a shop | | | | |
| Email spam folder | | | | |
| Speech-to-text dictation | | | | |

*Done looks like:* all 8 rows filled, every input and output named concretely (not "data"), and every reason mentions either "a human wrote the steps" or "it learned from examples".

**[Build] 3 — The 24-hour five.**
List **five** AI systems you personally touched in the last 24 hours. For each, write three things: (a) what it takes in, (b) what it puts out, (c) **what it is guessing**. Be precise about (c) — "it guesses what I want" is too vague; "it guesses which of 40 videos I am most likely to watch for over 30 seconds" is right.
*Done looks like:* 5 systems, all genuinely used by you, and 5 guesses each written as a specific prediction.

**[Build] 4 — Break a rule-based system.**
Pick one rule-based system from your own life (an alarm clock, a school bell, an autocorrect word list, a parental screen-time limit, a game's difficulty setting). Write down its rules as if-then statements — at least 3. Then invent **two real situations** where following those rules gives a clearly bad result.
*Done looks like:* 3+ if-then rules written out, plus 2 failure situations, each explaining which specific rule caused the bad outcome.

**[Stretch] 5 — The impossible rulebook.**
Choose one of these jobs: (a) decide if a photo shows a birthday party, (b) decide if a text message is sarcastic, (c) decide if a sound is a doorbell or a phone.
Try seriously to write if-then rules for it. Write at least 5. Then, for each rule, write a real-world case that breaks it.
*Done looks like:* 5 rules, 5 counterexamples, and a closing paragraph (4+ sentences) explaining why adding a 6th, 7th, and 8th rule would not fix it.

**[Stretch] 6 — The narrowness proof.**
Pick one AI system you can actually use today. Design and run **three tests** meant to find the edge of its narrowness — three requests that are slightly outside its one job. Record what it did.
*Done looks like:* a 3-row table (`request | what I expected | what it actually did`), plus one sentence stating what that system's single job really is, based on your evidence — not on its marketing.

---

## 🤔 Think Deeper

**1. If a machine's answer is right every time, does it matter whether it "understands"?**
A calculator is right about arithmetic 100% of the time and understands nothing. A doctor who understands deeply is still sometimes wrong. So does understanding matter, or only accuracy?
*How to reason about it:* separate two questions — (a) does understanding change how often it's right on cases it has seen before? and (b) does understanding change how it behaves on a case *nobody has ever seen*? Look for situations where those two answers differ. That gap is where your argument lives.

**2. When a rule-based system and a learned system disagree, which should a human trust?**
A school's rule-based system says a student is absent (no card swipe). A learned system says present (a camera recognised her face). Who decides?
*How to reason about it:* ask what each system can be *wrong* about and how you'd find out. Rule-based failures are usually explainable after the fact ("the card reader was broken"). Learned-system failures often aren't. Now ask: which is worse — a mistake you can explain, or a mistake you cannot? Does your answer change if the decision is a school register versus a prison sentence?

**3. We call it "artificial intelligence" — is that name doing harm?**
The name makes people imagine a mind. Suppose it had been called "automated pattern-matching" instead. Would people trust it more, or less, than they should?
*How to reason about it:* find two real situations — one where the grand name makes people trust it *too much*, and one where a boring name would make people dismiss something genuinely useful. Weigh both. Also consider who benefits from each name.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| "It's AI because it's on a computer / on the internet" | Everything modern feels like AI, so the word gets stuck on anything digital | Ask the judgement test first: would two reasonable people disagree about the answer? A calculator app is on a computer and is not AI |
| "It's AI because it talks / has a voice" | Voices feel like minds | A voice is just an output format. A talking clock is rule-based. Ignore the packaging; trace the input and the output |
| Confusing "it learns" with "it changes" | People assume anything that adapts is learning | Ask: did the *rule* change, or just the *setting*? A thermostat you set to 22°C changed a setting. A spam filter that started catching a new scam changed its rule |
| Treating a high confidence score as proof it's right | The number looks like a grade, and grades mean correctness | Confidence is the model's guess strength, not its accuracy. A model can be 98% confident and completely wrong. You'll measure this yourself in Module 6 |
| Calling every AI "generative" because chatbots are famous | Chatbots got all the news coverage, so "AI" now means "chatbot" to many people | Count the possible outputs. A short fixed menu means labelling; a blank page means generating |
| Believing today's AI is "close to" being a person | Movies, and the fact that fluent text feels like a mind | Run the job-count test: how many *different* jobs can it do? Every real system today answers 1 |
| Saying "the AI decided" as if nobody is responsible | It's a comfortable way to avoid blame | Every model was built by people, on data chosen by people, and deployed by people. Name them. Module 9 is built on this |

---

## 🛠️ Mini-Project — AI Spotter's Log

**Time: ~2.5 hours, spread across one full day.**

### 🎯 Goal

Over 24 hours, log **15 systems** you actually interact with. For each, record what it takes in, what it puts out, and which family it belongs to. Then defend your **3 hardest calls** in writing.

This is the project that turns the module from something you read into something you can *see*, everywhere, permanently.

---

### 📋 Starter steps

**Step 1 — Make the log sheet (10 min).**
On paper or in a spreadsheet, make these seven columns:

| # | System (be specific) | Where I met it | INPUT (what goes in) | OUTPUT (what comes out) | Family | Why (one line) |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

Rules for the columns:

- **System** must be specific. Not "my phone" — "my phone's keyboard suggestion bar".
- **Input** must be a concrete thing, not "data". Write "the last 3 words I typed", not "text".
- **Output** must be a concrete thing. Write "3 suggested next words", not "suggestions".
- **Family** must be exactly one of: `rule-based`, `machine learning`, `generative AI`, `not AI`.

**Step 2 — Hunt in four zones (60 min of real life, not desk time).**
Aim for at least 3 systems from each zone so you don't get 15 phone apps:

| Zone | Places to look |
|---|---|
| 🏠 Home | TV recommendations, smart speaker, washing machine cycles, thermostat, fridge, microwave, robot vacuum, doorbell |
| 📱 Phone/computer | keyboard autocorrect, photo search, face unlock, maps route, spam folder, video feed, music shuffle, translate, screen brightness |
| 🏫 School | attendance system, library scanner, plagiarism checker, grading software, timetable generator, projector auto-focus, school bell |
| 🛣️ Street/shop | traffic lights, self-checkout scanner, ATM, automatic doors, number-plate cameras, bus arrival board, escalator sensor |

**Step 3 — Fill 15 rows (45 min).** Do them as you meet them, not from memory at the end. Memory will give you the famous ones only.

**Step 4 — Mark your 3 hardest calls (5 min).** Put a ⭐ next to the three rows you were least sure about. Genuinely least sure — not the three most interesting.

**Step 5 — Write 3 defences (30 min).** One paragraph each, 5+ sentences. Every defence must contain all four of these:

1. What made it hard to classify.
2. The evidence *for* your answer.
3. The evidence *against* your answer — the honest case for the other side.
4. What single fact you would need to look up to be certain.

Point 4 is the one people skip, and it's the most valuable. "I would need to know whether the manufacturer trained it on recordings or hand-coded the wake word" is a real, answerable question.

---

### 🌟 Example of a good defence (use this as your standard)

> ⭐ **Row 7 — Self-checkout scanner at the supermarket.**
>
> This was hard because the machine does two very different jobs and I logged them as one. Reading the barcode is definitely rule-based: a barcode is a printed number, the scanner reads the black-and-white bars and looks the number up in a price table. A human designed that whole system, and the same barcode always gives the same price — no judgement anywhere. But the machine *also* watched the weight on the bagging plate and complained "unexpected item in bagging area" when my bag shifted. I first assumed that part was learned, because it seemed to be making a judgement about my behaviour.
>
> Evidence for rule-based: the complaint triggered the moment the weight changed by a small amount, and it triggered on a completely harmless movement. That's the fingerprint of a simple threshold — `IF weight_change > X AND no_item_scanned THEN alert`. A learned system trained on real shoppers would have seen thousands of harmless bag-shifts and would not flag them.
>
> Evidence against: modern supermarkets do use cameras for theft detection, and if this shop's system used the camera, that part would be machine learning, because no human can write if-then rules over camera pixels.
>
> **My call: rule-based**, because the false alarm was too crude to be learned. **What I'd need to know:** whether the overhead camera feeds into the same alert, or is only recording for staff to watch later. I could ask a staff member.

Notice what that paragraph does: it splits one product into two systems, uses the *behaviour* of the failure as evidence, and names a specific fact that would settle it.

---

### ✅ Success criteria checklist

- [ ] Exactly 15 rows, all filled in — no blanks
- [ ] At least 3 rows from each of the four zones (home, phone, school, street)
- [ ] Every row has a concrete input (not "data" or "information")
- [ ] Every row has a concrete output (not "a result")
- [ ] Every row has one of the four family labels
- [ ] At least 2 rows labelled `rule-based`
- [ ] At least 2 rows labelled `machine learning`
- [ ] At least 1 row labelled `generative AI` **or** a written note explaining why you met none
- [ ] At least 1 row labelled `not AI` (there will be — a light switch is not AI)
- [ ] 3 rows marked ⭐
- [ ] 3 written defences, 5+ sentences each, each containing all four required points

---

### 🚀 Level it up

**Interview an adult.** Show your log to a parent, teacher, or older sibling. Ask them to classify five of your rows *before* you show them your answer. Record where they disagreed with you.

Then write a short note answering: **were their disagreements mostly about the same kind of system?** Most adults over-guess "machine learning" for anything with a screen, and under-guess it for anything mechanical. If you find that pattern in your data, you have found something real about how people think about AI — and that's a genuine little research result you produced yourself.

---

## 🔑 Key Takeaways

- **AI is getting a machine to do a job that used to need a person's judgement.** No "smart", no "brain", no magic.
- **The sorting test has two questions:** (1) did a human write the rules, or did the machine learn them from examples? (2) if learned — does it output a label from a menu, or new content from a blank page?
- **Rule-based systems are predictable and explainable but brittle** — they only know what a human put in them, and they break silently on cases nobody anticipated.
- **Machine learning finds the rule from examples**, which means it can handle jobs no human could write rules for — and it is only as good as the examples it was given.
- **Generative AI is a kind of machine learning**, not a separate family. It produces new content instead of picking a label.
- **Every real AI system today is narrow**: one job, blank outside it. General AI does not exist.
- **Confidence is not correctness.** A system can be certain and wrong, and today's AI cannot reliably tell you when it's out of its depth.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Artificial intelligence (AI)** | A machine doing a job that used to need a person's judgement | A camera at a gate deciding which cars to let in |
| **Judgement** | A choice where reasonable people could disagree, and the answer depends on the specific case | "Is this photo blurry enough to delete?" |
| **Rule-based system** | A system where a human wrote the if-then steps by hand, in advance | A thermostat: `IF colder than 20°C THEN heat` |
| **If-then rule** | An instruction of the form "if this is true, do that" | `IF the word is not in the dictionary THEN underline it` |
| **Machine learning (ML)** | The machine works out the rule itself by studying labelled examples | A spam filter that learned "FREE + !!!" from 6 example messages |
| **Example** | One thing you show the machine, with the correct answer attached | One text message plus the note "this one is spam" |
| **Model** | The guessing machine that comes out of learning; feed it a new input, get a guess | The finished spam filter |
| **Label** | The answer a system gives when picking from a fixed set of options | `spam` or `not spam` |
| **Generative AI** | A system that makes new content instead of picking from a menu | A chatbot writing a poem nobody has written before |
| **Narrow AI** | A system that can do exactly one job and is blank outside it | AlphaGo, which plays Go and cannot play checkers |
| **General AI (AGI)** | An imaginary system that could do any job a person can. It does not exist today | Only in films |
| **Confidence score** | How strongly the model backs its own guess — a number, not a promise | "Dog: 94%" on a photo that is actually a fox |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — The one-sentence definition

**Model answer:**

> Artificial intelligence is when a machine does a job that used to need a person to look at a situation and decide.

**Why it works:** 20 words. No banned words. It contains the two load-bearing ideas — *used to need a person* and *decide* (judgement). A 7-year-old can follow it.

**Other acceptable answers:**

> AI is a machine that makes choices humans used to have to make, like sorting messages or spotting faces in photos.

> Artificial intelligence means a machine handles a decision that used to be a person's job.

**Answers that would NOT pass, and why:**

| Attempt | Problem |
|---|---|
| "AI is a computer that thinks like a person." | Uses *thinks*, and it's false — machines don't do it the human way |
| "AI is a very advanced computer program." | Doesn't mention decisions or judgement. A weather simulation is advanced and isn't AI |
| "AI is when a robot does what a human does." | Robots are bodies, not AI. Most AI has no body at all |
| "AI is technology that learns." | Too narrow — it excludes rule-based AI, and too vague otherwise |

---

### Exercise 2 — Sort the eight

| System | Input | Output | Family | Reason |
|---|---|---|---|---|
| Calculator app | Two numbers and an operation | One exact number | **not AI** | No judgement — one correct answer, one exact method |
| Phone face unlock | A camera image of a face | `unlock` or `stay locked` | **machine learning** | No human could write if-then rules over face pixels; trained on face images |
| Microwave timer | A number of seconds | A beep when it reaches zero | **not AI** | Counting down is not judgement |
| Netflix "because you watched…" | Your watch history + millions of other people's | A ranked list of shows | **machine learning** | Learned which shows go together from viewing patterns; nobody wrote those pairings by hand |
| Chatbot writing a poem | Your typed request | New text nobody wrote before | **generative AI** | Learned from examples AND its output is a blank page, not a menu |
| Automatic doors at a shop | A motion or infrared sensor reading | `open` or `stay shut` | **not AI** | `IF motion detected THEN open` — a human wrote it, and detecting motion isn't judgement. (Rule-based, yes — but rule-based systems only count as AI when the job needs judgement, and "did something move?" doesn't.) |
| Email spam folder | An email's words, sender, and links | `inbox` or `spam` | **machine learning** | Modern filters learn from billions of emails people marked as spam. (Note: a 1998 filter that only checked a banned-word list would be **rule-based** — same product, different era.) |
| Speech-to-text dictation | A sound recording | Written words | **machine learning** | Learned the sound-to-word mapping from recordings; no human can write rules over sound waves |

**The two rows worth arguing about:**

- **Automatic doors.** Some learners will say "rule-based AI". That's defensible if you argue that "is a person approaching?" involves judgement. The stronger argument is that a passive infrared sensor makes no case-by-case decision — it fires on any warm moving object, including a stray cat. No judgement, so `not AI`. Either answer is acceptable **if you gave that reasoning**.
- **Spam folder.** If you wrote `rule-based`, you're describing a filter from 25 years ago. Today's are learned. Full marks if you noted that it depends on the era.

---

### Exercise 3 — The 24-hour five

**Model answer (yours will differ — the *shape* is what matters):**

| # | System | Takes in | Puts out | What it is guessing |
|---|---|---|---|---|
| 1 | Phone keyboard suggestion bar | The last 2–3 words I typed | 3 suggested next words | It guesses which word I am most likely to type next, out of the ~50,000 words it knows |
| 2 | YouTube home feed | Everything I've watched, paused, and skipped | ~20 thumbnails in a chosen order | It guesses which video I am most likely to click and watch for more than 30 seconds |
| 3 | Phone face unlock | A camera image of my face | `unlock` / `stay locked` | It guesses whether this face is the owner's face, as a similarity score against a stored pattern |
| 4 | Google Maps route | My start, my destination, live traffic | A route and an arrival time | It guesses how many minutes each road segment will take right now, based on how long it took cars just before me |
| 5 | Spotify autoplay | The song that just finished + my history | The next song | It guesses which song I am least likely to skip in the first 20 seconds |

**Marking your own work:** cover the last column and read only "what it is guessing". Each line should read like a **prediction about a specific future event** — a click, a skip, a match, a number of minutes. If any of yours reads like "it guesses what I like", rewrite it. *Liking* is not measurable; *watching for 30 seconds* is. Real systems are always built around something measurable.

---

### Exercise 4 — Break a rule-based system

**Model answer: a school's screen-time app.**

**The rules:**

```
RULE 1: IF total screen time today > 120 minutes  THEN lock all apps
RULE 2: IF the current time is between 21:00 and 07:00  THEN lock all apps
RULE 3: IF the app is on the "education" list  THEN don't count its minutes
```

**Failure situation 1 — the homework lockout.**
I had a group project due tomorrow and used a video-call app for 40 minutes to work on it with two classmates. That app is not on the education list, so Rule 3 didn't protect it, and Rule 1 locked my phone mid-call at exactly 120 minutes. **The rule that caused it:** Rule 1, combined with Rule 3's list being incomplete. The rule counts *minutes*, but what actually matters is *what I was doing with them* — and minutes are easy for a computer to measure while purpose is not. That gap is exactly why the rule fails.

**Failure situation 2 — the 9pm emergency.**
My bus home was cancelled at 21:10. Rule 2 had already locked everything, including maps and messages, so I couldn't tell anyone or check the next bus. **The rule that caused it:** Rule 2, which uses a fixed clock time with no exceptions. A human parent would instantly grant an exception. The rule has no concept of "emergency" because nobody wrote one, and nobody wrote one because you cannot list every emergency in advance.

**Notice the pattern in both failures.** The rule measures something easy (minutes, clock time) and *assumes* it stands in for something hard (wasting time, needing sleep). Every rule-based failure in this course will have that same shape.

---

### Exercise 5 — The impossible rulebook

**Model answer for (b): decide if a text message is sarcastic.**

| # | Rule | A case that breaks it |
|---|---|---|
| 1 | `IF the message contains "yeah right" THEN sarcastic` | "Turn left at the lights, yeah right at the roundabout" — literal directions |
| 2 | `IF the message contains "🙄" THEN sarcastic` | "My little brother put 🙄 in every message this week, he thinks it means 'okay'" — a sincere complaint |
| 3 | `IF the message praises something after bad news THEN sarcastic` | "Failed my exam. Mum still made my favourite dinner, she's the best." — completely sincere |
| 4 | `IF the message uses ALL CAPS THEN sarcastic` | "MY SISTER GOT INTO MEDICAL SCHOOL!!!" — sincere excitement |
| 5 | `IF the message says "great" about a bad event THEN sarcastic` | "The fire alarm went off and we found the actual fire — great catch by whoever pulled it." — sincere praise |

**Closing paragraph:**

Adding more rules cannot fix this, and the reason is not that I haven't thought of enough rules. It's that sarcasm is not a property of the words at all. The exact same eight words — "oh brilliant, another maths test on Monday" — are sarcastic from someone who hates maths and sincere from someone who loves it and needs the grade. Nothing inside the message distinguishes those two cases. To get it right you need to know who sent it, what they usually think, what just happened to them, and what the two of you have joked about before. That information is not in the text, so no rule that reads only the text can reach it. Worse, every rule I add creates new false alarms: Rule 4 (ALL CAPS) would now flag every excited birthday message my whole family sends. Each new rule catches a few more true cases and wrongly catches many more false ones — and with fifteen or twenty rules, they start contradicting each other and I'd need rules about which rule wins. This is exactly the situation where you stop writing rules, collect a few thousand messages that real people have labelled sarcastic or sincere, and let a machine find the pattern instead. It still won't be perfect — but it will be better than my five rules, and it will get better as I add examples, which my rulebook never does.

---

### Exercise 6 — The narrowness proof

**Model answer: testing Quick, Draw!**

| Request | What I expected | What it actually did |
|---|---|---|
| Drew a **perfect circle** when asked for "sun" | Recognise it as a sun | Guessed "circle", then "clock", then "donut" — never got to sun until I added rays. It has no idea what a sun *is*; it only knows what people's sun drawings look like, and people always draw rays |
| Drew a **cat** when it asked for "dog" | Fail, then maybe say "that's a cat" | Guessed "dog" wrongly for the first 6 seconds, then said nothing. It never once said "cat" — because it is only ever checking against the one prompt it gave me. It can't volunteer what it actually sees |
| Wrote the **word "house"** in letters when asked for "house" | Fail — obviously | Guessed "zigzag", then "squiggle". Zero recognition that letters spelling H-O-U-S-E mean a house. Meaning is completely outside its world |

**Its single real job, from my evidence:**

> Quick, Draw! does one job: given a set of pen strokes and one target word, output how closely those strokes match the strokes other people drew for that same word. It is not recognising objects. It is matching stroke patterns to a stored prompt.

**Why this matters:** the marketing calls it "a **neural network** learning to recognise doodles" — a neural network is just a very large pile of adjustable numbers that gets tuned by examples, and you will build one yourself in Level 3. My three tests show it is not recognising anything — test 2 proves it, because a system that recognises objects would have said "that's a cat". It scores strokes against one target. That is a much smaller, much more honest description, and I got it by pushing three inches past the edge of the demo.

---

</details>

---

[⬅ Previous](../../CURRICULUM_MAP.md) · [Level 1 Home](README.md) · [Next ➡](module-02-data-is-everywhere.md)

*Next up: everything an AI knows arrived as **data**. In Module 2 you'll learn to turn any pile of real-world things into an honest table — one row per example, one column per thing you measured — and to spot the lies hiding in it.*

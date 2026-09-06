# 📓 Level 1 — Glossary

**Every term introduced in Level 1, alphabetized.** Plain English first, then an example taken from this course so you can go back and find where you met it.

[⬅ Level 1 Home](README.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Curriculum map](../../CURRICULUM_MAP.md)

---

## 🧭 How To Use This

- **Column 3 is the important one.** A definition you can recite is worth much less than an example you can point at. If the example doesn't ring a bell, go back to that module.
- **Column 4 tells you where it lives.** `M5` means Module 5. `Cap` means the capstone.
- If a word is used *before* it appears here, that's a bug in the course — tell someone.

**Jump to:** [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w)

---

## A

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Absolute value** | A number with its minus sign taken off. Written between two vertical bars. | The absolute value of −765 is 765 — used so an edge counts the same whether it goes dark→bright or bright→dark | M7 |
| **Accuracy** | Correct guesses divided by total guesses. Always say it as a fraction so people know how many things you tested. | 11 out of 15 = 11/15 = 0.733 = 73.3% | M3, M6 |
| **Accuracy gap** | The best group's accuracy minus the worst group's, measured in percentage points. The single number that exposes bias. | 91.7% in daylight − 41.7% held in a hand = a gap of 50.0 percentage points | M9 |
| **Anti-aliasing** | The soft grey in-between pixels a camera puts along the boundary of a shape, because the boundary doesn't land neatly on the pixel grid. | The 128s along the edge of your hand-drawn letter L on graph paper | M7 |
| **Artificial intelligence (AI)** | Getting a machine to do a job that used to need a person's judgement. Not "smart". Not a "brain". | A camera at a school gate deciding which cars to let in | M1 |
| **Attribution** | Saying who made something, where it came from, and who gave permission for it to be used. | "20 photos from my brother, with his permission, taken 4 March" in your data card | M9 |
| **Automation bias** | Trusting the machine's answer over your own judgement, just because a machine said it. | Following the satnav into a river because the screen said turn left | M9 |

---

## B

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Baseline** | The score you'd get by always guessing the most common answer. The number your model has to beat before it has done anything at all. | Three roughly equal classes → blind guessing scores 1/3 = 33.3% | M4, M6 |
| **Baseline model** | Your good, unmodified model — the one you compare every experiment against. | The 40-photos-per-class model scoring 91 / 88 / 79, saved as `baseline.tm` | M5 |
| **Bias** *(in machine learning)* | When a model works noticeably worse for some group of inputs than for others, in a way that matters. It is not an opinion — it is a measurable gap. | A model at 91% in daylight and 42% under a lamp | M9 |
| **Bigram** | Two tokens that appeared next to each other, in order. `the → cat` and `cat → the` are different bigrams. | `the → cat` appeared twice in the four-sentence corpus | M8 |
| **Binary classification** | Classification with exactly two boxes. | spam / not spam · locked / unlocked | M4 |
| **Bucketing** | Turning a number into categories by grouping ranges, which turns a regression task into a classification task. | 47 minutes of homework → the bucket "30–60 min" | M4 |

---

## C

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Category** | A value that names a group. Adding two of them together is meaningless. | `beagle`, `6A`, postcode `560001` — you cannot average postcodes | M2 |
| **Channel** | One of the three stacked number grids in a colour image. | The "red channel" is the whole grid of just the R numbers | M7 |
| **Class** | One of the named boxes a classifier can choose from. | `spoon` is one class of three | M4, M5 |
| **Class balance** | Whether each class has roughly the same number of training examples. | 41 / 40 / 39 is balanced. 200 / 200 / 8 is not. Target: (biggest − smallest) ÷ biggest under 20% | M5 |
| **Classification** | Predicting which box something goes in, from a short fixed list. | apple / orange / banana | M4 |
| **Clipping** | Forcing numbers back into the 0–255 range so they can be displayed as pixels. | A filter output of 1020 clipped by `MIN(255, …)` becomes 255 | M7 |
| **Column** | One attribute measured for every example. | `age_years`, recorded for all 30 students | M2 |
| **Condition** | The testable part of a rule — the bit that comes after IF. | `more than 50% of the letters are capitals` | M3 |
| **Confidence score** | How strongly the model prefers each class. The scores always add to 100%. It is a guess *strength*, not a promise of correctness. | `spoon 62%, toothbrush 21%, comb 17%` | M1, M5 |
| **Confidence threshold** | A cut-off you set: below this confidence, the system says "not sure" instead of guessing. | A booth app that refuses to answer below 70% | Cap |
| **Confusion matrix** | A grid with the true class down the side and the predicted class across the top, so you can see exactly what got mistaken for what. | 5/0/0 · 0/4/1 · 1/2/2 — which shows combs being called toothbrushes | M6 |
| **Context** | How many previous words a language model is allowed to look at when guessing the next one. | A bigram model sees 1 word. A real chatbot sees thousands. | M8 |
| **Controlled experiment** | Changing exactly one thing and keeping everything else identical, so you know what caused the result. | Same objects, same room, same order — only the photo count changed | M5 |
| **Controlled vocabulary** | The written list of allowed values for a category column, so `blue` and `Blue` don't become two things. | `main_food` may only be one of six listed foods | M2 |
| **Corpus** | The pile of text you learn from. | The four sentences about the cat and the dog | M8 |

---

## D

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Data** | Observations written down in a form a machine can read. | `2026-09-02, rain, 18°C` | M2 |
| **Data card** | A short, honest note describing a dataset: what it is, how much, from whom, with what permission, what's **not** in it, and its known limits. | The eight-box card printed and put on your fair booth table | M2, Cap |
| **Data type** | What kind of value a column holds, which decides what you're allowed to do with it. | `sleep_hours` is a number; `favourite_colour` is a category | M2 |
| **Deepfake** | A fake photo, video, or voice of a real person, generated by AI. | A video of an athlete saying something they never said | M9 |
| **Default** | The answer a rulebook gives when no rule fires. | `OTHERWISE → ham` at the bottom of the spam rulebook | M3 |
| **Diagonal** | The cells of a confusion matrix where the true class equals the predicted class — the correct answers. | 5 + 4 + 2 = 11 correct out of 15 | M6 |
| **Disinformation** | False information spread **deliberately** to deceive. | A fake video made and posted to swing an election | M9 |
| **Downsampling** | Shrinking an image by averaging blocks of pixels into single pixels, which throws information away. | Four pixels 255, 0, 0, 255 average to 127.5 | M7 |
| **Duplicate** | The same example recorded more than once. | Saturday listed twice with identical values | M2 |

---

## E

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Edge** | A place in an image where brightness changes suddenly. The first genuinely useful thing a vision system finds. | The border between a dark comb and a white table | M7 |
| **Edge case** | An example your rule gets wrong, usually sitting right next to a boundary you chose. | A 138 cm teenager turned away from a ride with a 140 cm limit | M3 |
| **Edge map** | The new grid you get after running an edge filter over an image — an outline drawing made of numbers. | The hollow square that appears from a solid white square | M7 |
| **Epoch** | One complete pass through every training example. | 50 epochs × 120 photos = 6,000 looks | M5 |
| **Error** *(in regression)* | How far a predicted number was from the true number. | Predicted 197.5 g, true 205 g → 7.5 g off | M4 |
| **Example** | One thing you show the machine, with the correct answer attached. | One text message plus the note "this one is spam" | M1 |
| **Exponential growth** | A quantity that doubles at every step, so it gets enormous much faster than people expect. | 2, 4, 8, 16… — 30 yes/no checks reach over a billion combinations | M3 |

---

## F

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Fairness audit** | Deliberately testing a model group by group, to find out who it fails, before they find out. | Four batches of 12 photos — control, new lighting, new hands, new background — each scored separately | M9 |
| **Fallback** | The reply a rule-based bot gives when nothing in its table matches. | "I don't know that one. Try asking about toppings." | M8 |
| **False alarm** | The system says yes when the truth is no. | A friend's message marked as spam | M3 |
| **False reject** | The system fails to recognise someone or something that really is there. | A present student marked absent by the face scanner | M9 |
| **Feature** | One measured description of one example. One column in your table. | `weight_g = 150` for the apple in row 1 | M4 |
| **Feature table** | A table where each row is an example, most columns are features, and one column is the label. | The 12-row fruit bowl table | M4 |
| **Filter (kernel)** | A small grid of numbers you slide over an image to highlight one particular thing. | `-1 0 +1` in three rows highlights vertical edges | M7 |
| **First match wins** | The convention that the first rule to fire decides the answer, so rule order matters. | Rule 1 beats Rule 4 even when both would fire | M3 |
| **Fresh examples** | Examples the system has never seen, used to score it honestly. | The 10 messages in the sealed envelope | M3 |

---

## G

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Gap, the** | Training accuracy minus test accuracy. How much memorising happened. | 100% − 73.3% = 26.7 points | M6 |
| **General AI (AGI)** | An imaginary system that could do any job a person can. **It does not exist today.** | Only in films | M1 |
| **Generalizing** | Working correctly on examples the model has never seen. The only thing you actually want. | 73.3% on the hidden photos | M6 |
| **Generative AI** | A system that makes new content — text, images, sound — instead of picking a label from a menu. | A chatbot writing a poem nobody has written before | M1 |
| **Grayscale** | A black-and-white image where each pixel is one brightness number. | 0 = black, 128 = grey, 255 = white | M7 |
| **Greedy** *(generation)* | Always picking the single most likely next word, never rolling the dice. | Tapping the middle keyboard suggestion every time — which is why it falls into loops | M8 |

---

## H

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Hallucination** | When an AI produces something that sounds completely right and simply isn't true. | "The cat ate the bone" — fluent, and not what the corpus said | M8 |
| **Header** | The top row of a table, which names each column. | The first row reading `name`, `age`, `class`, `present` | M2 |
| **Hold out** | To deliberately set examples aside **before** training, and never train on them. | "I held out 5 photos per class, in a separate folder" | M6 |

---

## I

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **If-then rule** | An instruction of the form "if this is true, do that". How humans normally program a computer. | `IF the word is not in the dictionary THEN underline it in red` | M1, M3 |
| **Impossible value** | A value that reality does not allow, which means it is an error. | `sleep_hours = 88`; `weight_kg = −5`; `age = 211` | M2 |

---

## J

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Judgement** | A choice where reasonable people could disagree, and the right answer depends on looking at the specific case. The word at the centre of the definition of AI. | "Is this photo blurry enough to delete?" — unlike 47 + 88, which has one exact answer | M1 |

---

## L

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Label** | The answer you want the machine to produce. The column you cover up. | `fruit = apple`; `spam` or `not spam` | M1, M4 |
| **Labelled example** | A piece of data with the correct answer written next to it. The raw material of all machine learning. | `"FREE money!!!" → spam` | M3 |
| **Language model** | A system that predicts likely next words. Your tally sheet is one. So is a chatbot — just enormously bigger. | The bigram table you built by hand from a 200-word paragraph | M8 |
| **Leaky feature** | A sneaky feature that already contains the answer, and won't exist when you actually need a prediction. You spot it by a suspiciously perfect score. | `sticker_says = APPLE`; `was_it_handed_in_late` | M4 |

---

## M

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Machine learning (ML)** | The machine finds the decision rule itself by studying many examples where someone already wrote down the correct answer. | A spam filter that worked out "FREE + !!!" from six example messages | M1 |
| **Machine learning trade, the** | Give up writing rules by hand; hand the machine labelled examples instead. You lose explainability and gain the ability to do jobs where nobody can state the rule. | 5,000 labelled messages instead of 258 hand-written rules | M3 |
| **Margin** | Top confidence score minus the second-highest. How close the race was. | 62 − 21 = 41 | M5 |
| **Measuring instruction** | The exact written recipe for getting a feature's value, so that anyone measuring gets the same number. | "ruler, longest straight dimension, to the nearest 0.5 cm" | M4 |
| **Megapixel** | One million pixels. | A 12-megapixel camera makes images of about 12,000,000 pixels | M7 |
| **Memorizing** | Working only on the exact examples the model studied, and falling apart on anything else. | 100% on training photos, 40% on new ones | M6 |
| **Metadata** | Hidden information a file carries about itself. | The GPS location and time stored inside a photo you posted | M9 |
| **Misinformation** | False information spreading, whether or not anyone meant to deceive. | An old photo reposted as if it happened today | M9 |
| **Miss** | The system says no when the truth is yes. The opposite mistake to a false alarm. | A bank scam landing safely in the inbox | M3 |
| **Missing value** | An empty box where a measurement should be. Mark it; never silently treat it as zero. | You forgot to record Wednesday's sleep | M2 |
| **Model** | The guessing machine that comes out of training. Feed it a new input, get a guess. | The `.tm` file you download from Teachable Machine | M1, M5 |
| **Multi-class classification** | Classification with three or more boxes. | apple / orange / banana | M4 |

---

## N

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Narrow AI** | A system that does exactly one job and is completely blank outside it. **Every real AI system today is narrow.** | AlphaGo, which plays Go and cannot play checkers | M1 |
| **Next-word prediction** | Guessing which word comes next, then repeating with the new word included. The engine behind autocomplete and every chatbot. | Tapping the middle suggestion on your phone keyboard 20 times | M8 |
| **N-gram** | Any run of *n* tokens in a row. A bigram is a 2-gram; a trigram is a 3-gram. | A 5-gram uses the previous four words to guess the fifth | M8 |
| **Number** *(data type)* | A value you can meaningfully add and average. | 7.5 hours of sleep — unlike a postcode, which only looks like a number | M2 |

---

## O

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Off-diagonal cell** | A cell of a confusion matrix showing a mistake — and showing exactly what got confused with what. | 2 combs called toothbrush | M6 |
| **`other` class** | An extra box for "none of the above", filled with random and background images so the model can refuse. | Empty hand, bare table, a fork, a wall | M5, Cap |
| **Outlier** | A **legal** value that sits far away from all the others. Not the same as an impossible value. | 480 screen-minutes in a week of values around 150 | M2 |
| **Overfitting** | Fitting the training examples so closely that the model stops working on new ones. In plain words: it learned the photos, not the object. | The one-background model: 95% on its own table, 34% two metres away at the sink | M6 |
| **Over-trust** | Accepting an AI answer without checking, because it sounded sure. | Copying a book title the AI invented straight into your homework | M9 |

---

## P

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Pattern** | Something that repeats often enough that betting on it beats guessing. | The 9:05 bus was late on 4 out of 4 Mondays | M3 |
| **Per-class accuracy** | Accuracy worked out separately for each class, instead of one number for everything. | spoon 100%, toothbrush 80%, comb 40% | M6 |
| **Percentage point** | The unit you get when you subtract one percentage from another. 41.7% rising to 91.7% is a rise of 50 **points**, not 50%. | A 49-point gap between daylight and lamplight accuracy | M6, M9 |
| **Personal data** | Information about an identifiable person. | A face photo, a phone number, a home postcode, a full name in a spreadsheet | M9 |
| **Pixel** | One tiny square of a picture — the smallest piece a computer stores. | A 5 × 5 image has 25 pixels | M7 |
| **Population** | Everything you want your answer to be true about. | All 800 students in the school | M2 |
| **Pre-registration** | Writing down what you expect, and what counts as success, **before** you run the test — so you can't move the goalposts afterwards. | "I will call it useful if it beats 60%", written in the brief before training | Cap |
| **Prompt** | The text you give a generative model to start from. | "Write me a poem about rain" | M8 |
| **Provenance** | The origin story of data: who collected it, from whom, when, how, and with what permission. | "Me, by hand, 24–30 Aug 2026, in a notebook" | M2, M9 |

---

## Q

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Quick, Draw!** | A free browser game where you doodle and a model guesses what you drew, trained on millions of other people's doodles. | Used to feel what "learned from examples" means before you train anything | M1, M7 |

---

## R

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Regression** | Predicting a number on a sliding scale, rather than picking a box. | "This orange weighs 197.5 g" | M4 |
| **Re-identification** | Working out who someone is from data that was supposed to be anonymous, by combining clues. | Year 7 + postcode + left-handed = exactly one person | M9 |
| **Resolution** | How many pixels an image has, written width × height. | 224 × 224 = 50,176 pixels — the size Teachable Machine shrinks your photos to | M7 |
| **RGB** | Storing colour as three numbers per pixel: how much red, green, and blue light. | (255, 255, 0) is yellow, because red light plus green light makes yellow | M7 |
| **Row** | One example — one single thing you observed. | One student on one day; one meal; one photo | M2 |
| **Rule-based system** | A system where a human wrote the decision steps by hand, as if-then instructions, before the machine ever ran. | A thermostat: `IF colder than 20°C THEN heat` | M1 |
| **Rule explosion** | The number of situations to cover grows far faster than the rules you can write, until the rulebook becomes impossible to maintain. | 30 yes/no checks give 2³⁰ ≈ 1.07 billion possible situations | M3 |
| **Rulebook** | An ordered list of if-then rules, plus a default for when none of them fire. | The five spam rules in Module 3's worked example | M3 |

---

## S

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Sabotage test** | Deliberately damaging your own training data to find out what the model was really depending on. | Retraining using photos from one background only, then testing elsewhere | M5 |
| **Sample** | The smaller set you actually measured. Your 30 rows are not the whole world. | The 30 students you asked, out of 800 | M2 |
| **Sampling** *(in generation)* | Picking randomly, weighted by the counts, rather than always taking the top choice. | Drawing one slip from a bag of 8, where 2 slips say `cat` | M8 |
| **Scratch** | A free block-based programming environment where you drag instructions together instead of typing code. | The PizzaBot chatbot and the fair booth app | M8, Cap |
| **Split ratio** | How you divided your examples between training and testing. | 80 / 20 — the usual default | M6 |

---

## T

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Table** | Data arranged in rows and columns. The universal shape of everything an AI learns from. | A class register | M2 |
| **Teachable Machine** | A free Google tool that trains an image, sound, or pose classifier **inside your browser**, with no code and no upload. | Where you trained your first three-class model | M5 |
| **Test set** | Examples you hide before training and use once, at the end, to find out how good the model really is. | 15 photos taken on a different day, sealed in an envelope | M6 |
| **Test-set leakage** | Slowly contaminating your test set by tweaking the model over and over based on its test score. Every tweak was chosen *because of* that score. | Test → tweak → retrain → test → tweak, five times, then reporting the final number as honest | M6 |
| **Threshold** | The cut-off number inside a condition. | The `2.0` in `IF hours_studied >= 2.0` | M3 |
| **Token** | One piece of chopped-up text — usually a word, sometimes a punctuation mark. | "I love pizza!" → `i`, `love`, `pizza`, `!` | M8 |
| **Tokenize** | To chop text into tokens. | Splitting a paragraph into a numbered list of 26 tokens | M8 |
| **Training** | The one-time process where a machine studies labelled examples and tunes itself until it can separate them. | 120 photos, 50 epochs, 22 seconds | M5 |
| **Training examples** | The labelled examples your rules or model were built from. Scoring on these proves nothing. | The 20 messages you wrote your spam rulebook from | M3 |
| **Training set** | The examples the model is allowed to study. | 60 of the 75 photos | M6 |
| **Trigram** | Three tokens in a row. | `(sat, on) → the` | M8 |

---

## U

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Underfitting** | The model learned almost nothing — it scores badly on the training examples *and* on new ones. A different disease from overfitting, with a different cure. | 58% training, 55% test: a 3-point gap and both numbers poor | M6 |
| **Unplugged** | An activity that teaches a computing idea with paper, pencil and people, and no computer at all. | Becoming a pixel grid on graph paper; the Feature Card Deck | M2, M4, M7 |
| **Useful feature** | A feature that makes your guess better than guessing blind. | `colour` scored 91.7% against a 33.3% baseline | M4 |
| **Useless feature** | A feature that makes no difference at all — its score sits on the baseline. | `quadrant` scored exactly 33.3%, the baseline | M4 |

---

## V

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Variety** | How much your training examples differ in the ways that *shouldn't* matter — background, lighting, angle, distance, who's holding it. | 5 backgrounds, 3 lightings, 8 angles for every class | M5 |

---

## W

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Word frequency** | How many times each word appears in a corpus. | `the` appeared 8 times out of 26 tokens — nearly a third of the text | M8 |

---

## 🔟 The Twenty That Matter Most

If you only truly own twenty of these, make it these. Everything in Level 2 is built directly on top of them.

```
   THE THING ITSELF            HOW IT LEARNS              HOW YOU MEASURE IT
   ─────────────────           ────────────────           ──────────────────
   1. artificial intelligence  6. training                11. training set
   2. rule-based system        7. model                   12. test set
   3. machine learning         8. labelled example        13. hold out
   4. narrow AI                9. class                   14. accuracy
   5. generative AI           10. confidence score        15. baseline

   HOW IT DESCRIBES THINGS     WHEN IT GOES WRONG
   ───────────────────────     ──────────────────
   16. feature                 18. overfitting
   17. label                   19. bias
                               20. accuracy gap
```

**The five-minute test.** Cover column 2 and 3 of this glossary. Go down that list of twenty and say each definition out loud with one example. Anything you stumble on, go back to its module. That's twenty words, five minutes, and it is the most efficient revision in this whole level.

---

## 🚫 Words We Deliberately Avoid

These are not in the glossary because this course does not use them about AI systems. Knowing *why* they're banned is worth as much as knowing the terms above.

| Banned word | Why we don't use it | Say this instead |
|---|---|---|
| **magic** | It's a way of saying "I have stopped explaining." Everything in this level has a mechanism you can point at. | "It found a pattern across 160 labelled photos." |
| **smart** | It compares the machine to a person and tells you nothing about what it does. A calculator is fast, not smart. | "It does a job that used to need judgement." |
| **brain** | Nothing inside these systems resembles a brain, and the metaphor is exactly what makes people over-trust them. | "A model — a guessing machine." |
| **it thinks / it understands / it knows** | These claim an inner life the system doesn't have, and they make the failures baffling instead of predictable. | "It predicts", "it matches a pattern", "it outputs". |
| **the AI figured it out** | Vague, and it hides the two things that actually explain the behaviour: the data and the training. | "It was trained on examples where…" |
| **obviously** | Usually a sign you're skipping the step you found hardest. | Show the arithmetic. |

---

[⬅ Level 1 Home](README.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Curriculum map](../../CURRICULUM_MAP.md) · [Level 2 ➡](../level-2-builder/)

*Around 130 terms. You met every one of them by building something. That's why they'll stick.*

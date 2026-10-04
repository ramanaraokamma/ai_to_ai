from notes import NOTEBOOK
from rag import chunk_by_heading, VectorIndex, TfidfEmbedder

chunks = chunk_by_heading(NOTEBOOK)
titles = [c.split("\n")[0][3:] for c in chunks]
print(f"{len(chunks)} chunks, {sum(len(c.split()) for c in chunks)} words total")

index = VectorIndex(chunks, TfidfEmbedder())
for cid, score, _ in index.search("Why did post-norm need warmup?", k=3):
    print(f"  {score:.3f}  [{cid}] {titles[cid]}")

QUERIES = [
    "how do I stop my training from blowing up at the start?",
    "which optimiser should I try first?",          # British spelling
    "what happens if the model cannot tell word order?",
    "how much does one API call cost?",
    "why did my loss become NaN?",
]

for q in QUERIES:
    print(f"\nQ: {q}")
    for cid, s, _ in index.search(q, k=3):
        print(f"   {s:.3f}  {titles[cid]}")

# Gold is an exact substring that must appear in a retrieved chunk.
# Defining gold this way lets one eval set score EVERY chunking strategy.
EVAL = [
    ("Which optimizer converged fastest and by how much?", "40 epochs"),
    ("What learning rate made the loss go to NaN?", "NaN by step 30"),
    ("Did dropout help more than weight decay?", "Weight decay 0.01"),
    ("What sampling temperature worked best for the name generator?", "Temperature 1.2"),
    ("How much does the scaling change the attention weights?", "0.52, 0.31, 0.17"),
    ("What happened to validation loss when positional information was removed?", "1.68 to 2.41"),
    ("Why did post-norm need warmup?", "Post-norm needed"),
    ("How many merges did the BPE tokenizer learn?", "138 merges"),
    ("What was the constant-answer baseline on the prompt bench?", "baseline was 43.8%"),
    ("How much does one extraction call cost in dollars?", "0.00144 dollars per call"),
]


def recall_at_k(index, evalset, ks=(1, 3)):
    out = {}
    for k in ks:
        hits = sum(any(marker in c for _, _, c in index.search(q, k=k))
                   for q, marker in evalset)
        out[k] = hits / len(evalset)
    return out


from rag import chunk_fixed
total_words = len(NOTEBOOK.split())
STRATS = [
    ("headings (whole notes)", chunk_by_heading(NOTEBOOK)),
    ("fixed 30w / 8 overlap", chunk_fixed(NOTEBOOK, 30, 8)),
    ("fixed 60w / 15 overlap", chunk_fixed(NOTEBOOK, 60, 15)),
    ("fixed 120w / 0 overlap", chunk_fixed(NOTEBOOK, 120, 0)),
    ("fixed 250w / 50 overlap", chunk_fixed(NOTEBOOK, 250, 50)),
]

print(f"{'strategy':25s} {'n':>3s} {'avg w':>6s} {'r@1':>5s} {'r@3':>5s} "
      f"{'ctx w @k=3':>11s} {'% corpus':>9s}")
for name, ch in STRATS:
    idx = VectorIndex(ch, TfidfEmbedder())
    r = recall_at_k(idx, EVAL)
    ctx = sum(sum(len(c.split()) for _, _, c in idx.search(q, k=3))
              for q, _ in EVAL) / len(EVAL)
    avg_w = sum(len(c.split()) for c in ch) / len(ch)
    print(f"{name:25s} {len(ch):3d} {avg_w:6.1f} {r[1]:5.2f} {r[3]:5.2f} "
          f"{ctx:11.0f} {ctx / total_words * 100:8.0f}%")

PARAPHRASED = [
    ("Which update rule got me to a good result in the fewest passes over the data?", 0),
    ("My numbers turned into not-a-number early on. Which step size caused that?", 1),
    ("Which regulariser gave the steadier held-out curve?", 2),
    ("What randomness setting produced the best made-up words?", 3),
    ("What breaks if I skip the division before the exponential normalisation?", 5),
    ("How badly does the model do if it cannot tell which token came first?", 7),
    ("Which normalisation order let me skip the slow start-up ramp?", 9),
    ("How many gluing steps did my subword vocabulary end up with?", 10),
    ("What score would a system get by ignoring the input entirely?", 13),
    ("What do I pay for a single request in cents?", 14),
]


def recall_by_id(index, evalset, ks=(1, 3, 5)):
    out = {}
    for k in ks:
        hits = sum(gold in [cid for cid, _, _ in index.search(q, k=k)]
                   for q, gold in evalset)
        out[k] = hits / len(evalset)
    return out


print("literal   wording, tfidf:", recall_by_id(index,
      [(q, i) for i, (q, _) in zip([0,1,2,3,5,7,9,10,13,14], EVAL)]))
print("paraphrased wording, tfidf:", recall_by_id(index, PARAPHRASED))

ANSWERABLE = [q for q, _ in EVAL]
UNANSWERABLE = [
    "What did I conclude about federated learning?",
    "Which GPU did I train the tiny GPT on?",
    "How many students are in my class?",
    "What is the capital of France?",
]

ans_scores = [index.search(q, 1)[0][1] for q in ANSWERABLE]
un_scores = [index.search(q, 1)[0][1] for q in UNANSWERABLE]
print("answerable  :", " ".join(f"{s:.3f}" for s in sorted(ans_scores)))
print("unanswerable:", " ".join(f"{s:.3f}" for s in sorted(un_scores)))

print(f"\n{'tau':>5s} {'answered':>10s} {'refused':>9s} {'errors':>7s}")
for tau in [0.05, 0.12, 0.15, 0.20, 0.25, 0.30]:
    a = sum(s >= tau for s in ans_scores)
    u = sum(s < tau for s in un_scores)
    print(f"{tau:5.2f} {a:8d}/10 {u:7d}/4 {(10 - a) + (4 - u):7d}")


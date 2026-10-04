import matplotlib; matplotlib.use('Agg')
from m06_lib import *
from m06_lib import recall_at_k
def recall_by_id(index, evalset, ks=(1, 3, 5)):
    out = {}
    for k in ks:
        hits = sum(gold in [cid for cid, _, _ in index.search(q, k=k)] for q, gold in evalset)
        out[k] = hits / len(evalset)
    return out
print('== ex1'); 
import numpy as np

u = np.array([3., 0., 4.]); v = np.array([6., 0., 8.])
w = np.array([0., 5., 0.]); x = np.array([-3., 0., -4.])

def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

print(f"cos(u,v) = {cos(u, v):.4f}")
print(f"cos(u,w) = {cos(u, w):.4f}")
print(f"cos(u,x) = {cos(u, x):.4f}")

un = u / np.linalg.norm(u)      # [0.6, 0.0, 0.8]
vn = v / np.linalg.norm(v)      # [0.6, 0.0, 0.8]
print(un, vn, float(un @ vn))   # -> 1.0

print('== ex2 zeros')
V = set(index.emb.v.get_feature_names_out())
analyze = index.emb.v.build_analyzer()

PROBES = [
    ("which regulariser stopped overfitting?", 2),        # gold: dropout / weight decay
    ("what happens with a huge minibatch?", 8),           # gold: batch size experiment
    ("what optimiser converged quickest?", 0),            # gold: optimizer bake-off
    ("how expensive is an enquiry?", 14),                 # gold: cost accounting
    ("was the tokeniser lossless?", 10),                  # gold: BPE tokenizer
    ("how fast did the recurrent unit run?", 4),          # control: should NOT be zero
]
for q, gold in PROBES:
    oov = [w for w in analyze(q) if w not in V]
    cid, s, _ = index.search(q, k=1)[0]
    print(f"  tfidf {s:.3f}  got [{cid}] {titles[cid][13:]:30s} want [{gold}]   oov={oov}")

print('== ex3 overlap')
import matplotlib.pyplot as plt
from rag import chunk_fixed, VectorIndex, TfidfEmbedder

rows = []
for ov in [0, 5, 10, 20, 30]:
    ch = chunk_fixed(NOTEBOOK, 40, ov)
    idx = VectorIndex(ch, TfidfEmbedder())
    r = recall_at_k(idx, EVAL, ks=(1, 3))
    stored = sum(len(c.split()) for c in ch)
    rows.append((ov, len(ch), r[1], r[3], stored))
    print(f"overlap {ov:2d}  chunks {len(ch):3d}  r@1 {r[1]:.2f}  r@3 {r[3]:.2f}  "
          f"words stored {stored:5d}  ({stored / len(NOTEBOOK.split()) * 100:.0f}% of source)")

plt.figure(figsize=(7, 4))
plt.plot([r[4] for r in rows], [r[2] for r in rows], "o-")
for ov, n, r1, r3, st in rows:
    plt.annotate(f"ov={ov}", (st, r1), textcoords="offset points", xytext=(6, 6))
plt.axvline(len(NOTEBOOK.split()), ls="--", c="crimson", label="original document size")
plt.xlabel("words stored in the index")
plt.ylabel("recall@1")
plt.title("Overlap sweep at 40-word chunks")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig("../out/overlap_sweep.png", dpi=80)

print('== ex4 2x2')
rows = []
for q, marker in EVAL:
    hits = index.search(q, k=3)
    retrieval_ok = any(marker in c for _, _, c in hits)
    r = ask(index, q, verbose=False)
    # crude but honest: does the answer contain the distinctive part of the marker?
    key = marker.split()[-1].rstrip(".,")
    generation_ok = key.lower() in r["answer"].lower()
    rows.append((q, retrieval_ok, generation_ok, r["answer"], [c for c, _, _ in hits]))

cells = {(True, True): [], (True, False): [], (False, True): [], (False, False): []}
for i, (q, ro, go, a, ids) in enumerate(rows, 1):
    cells[(ro, go)].append(i)

print("                      generation OK   generation WRONG")
print(f"retrieval OK      {len(cells[(True, True)]):10d} {len(cells[(True, False)]):17d}")
print(f"retrieval FAILED  {len(cells[(False, True)]):10d} {len(cells[(False, False)]):17d}")
for k, v in cells.items():
    print(f"  {k}: questions {v}")

print('== ex6 poison')
POISON = """
## 2026-09-01 — Learning rate revisited
Re-ran the learning rate sweep with the fixed data loader. This time 1e-2 was clearly
best, not 1e-3. The earlier 1e-3 result was an artefact of the shuffling bug.
"""
poisoned = chunk_by_heading(NOTEBOOK + POISON)
pidx = VectorIndex(poisoned, TfidfEmbedder())

for cid, s, _ in pidx.search("What learning rate was best?", k=3):
    print(f"  {s:.3f}  [{cid}] {poisoned[cid].splitlines()[0][3:]}")

# ex5 (hybrid) needs MiniLM -> only the alpha=0 (pure tfidf) row is reproducible offline
LIT=list(zip([q for q,_ in EVAL],[0,1,2,3,5,7,9,10,13,14]))
PARAPHRASED=[("Which update rule got me to a good result in the fewest passes over the data?",0),("My numbers turned into not-a-number early on. Which step size caused that?",1),("Which regulariser gave the steadier held-out curve?",2),("What randomness setting produced the best made-up words?",3),("What breaks if I skip the division before the exponential normalisation?",5),("How badly does the model do if it cannot tell which token came first?",7),("Which normalisation order let me skip the slow start-up ramp?",9),("How many gluing steps did my subword vocabulary end up with?",10),("What score would a system get by ignoring the input entirely?",13),("What do I pay for a single request in cents?",14)]
IDENT=[("Which attention head looked at the previous character?",6),("What happened at learning rate 1e-1?",1),("What is 0.00144 dollars per what?",14)]
print("tfidf-only (alpha=0): literal",recall_by_id(index,LIT,ks=(1,))[1],"paraphrase",recall_by_id(index,PARAPHRASED,ks=(1,))[1],"identifier",recall_by_id(index,IDENT,ks=(1,))[1])
print("TF-IDF score range on answerable top-1:", min(index.search(q,1)[0][1] for q in ANSWERABLE), max(index.search(q,1)[0][1] for q in ANSWERABLE))

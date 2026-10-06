"""Every number the shared motifs print, in one place, each with its provenance.

Rule (STYLE.md 2.1): a number on a Level 4 canvas is (a) printed by an executed seeded run,
(b) a hand calculation whose sum is printed beside it, or (c) a quoted figure. This module
is the audit trail. Nothing here is invented.

  DEMO      - computed below by numpy, seed 0, deterministic (kind a: this file IS the run)
  LEDGER    - copied from the executed ledger outputs in ../../_ledger/out (kind a)
  HAND      - plain arithmetic, the sum is printed on the canvas (kind b)
"""
import math
import numpy as np

# ---------------------------------------------------------------- DEMO: logistic regression, seed 0
# Full-batch gradient descent on 200 seeded points in 2-D (two blobs), 40 steps, three learning
# rates. Weights start at zero so every run's first loss is exactly ln 2 = 0.693.
DEMO_SEED = 0
DEMO_STEPS = 40
DEMO_LRS = (0.02, 0.2, 1.0)


def _demo():
    rng = np.random.default_rng(DEMO_SEED)
    n = 100
    X = np.vstack([rng.normal(-1.0, 1.0, (n, 2)), rng.normal(1.0, 1.0, (n, 2))])
    y = np.concatenate([np.zeros(n), np.ones(n)])
    curves = {}
    for lr in DEMO_LRS:
        w = np.zeros(2)
        b = 0.0
        ls = []
        for _ in range(DEMO_STEPS + 1):
            p = 1.0 / (1.0 + np.exp(-(X @ w + b)))
            ls.append(float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))))
            g = p - y
            w = w - lr * (X.T @ g) / len(y)
            b = b - lr * float(np.mean(g))
        curves[lr] = ls
    return curves


DEMO = _demo()
LN2 = math.log(2.0)                                  # 0.6931..., printed as 0.693

# ---------------------------------------------------------------- LEDGER: TinyGPT seed 1337 (Week 17)
# m03_01_tiny_gpt.txt: 807,196 parameters, 6972 characters.
GPT_STEPS = [0, 500, 1000, 1500, 2000, 2499]
GPT_TRAIN = [3.340, 1.226, 0.445, 0.212, 0.159, 0.148]
GPT_VAL = [3.335, 1.410, 1.328, 1.589, 1.664, 1.682]
GPT_GAP = round(GPT_VAL[-1] - GPT_TRAIN[-1], 3)     # HAND: 1.682 - 0.148 = 1.534

# m03_05_ablate_*.txt: 1,500 steps each. best val and where; final train/val.
ABLATE = [  # name, best val, best step, final train, final val
    ("baseline", 1.278, 750, 0.411, 1.336),
    ("no residual", 2.848, 850, 2.843, 2.849),
    ("no scale", 1.245, 600, 0.278, 1.352),
]

# ---------------------------------------------------------------- LEDGER: Week 14 attention (hand pass)
ATT_TOKENS = ["the", "cat", "sat"]
ATT_W = [[0.4223, 0.1554, 0.4223],
         [0.1554, 0.4223, 0.4223],
         [0.2119, 0.2119, 0.5761]]                   # weights, four places (Week 14 key)
ATT_SCORES = [[1, 0, 1], [0, 1, 1], [1, 1, 2]]
ATT_OUT = [[0.578, 0.845], [0.845, 0.578], [0.788, 0.788]]
ATT_V = [[0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]

# Week 15 (teacher-only box): divide by sqrt(2) AND mask the future -> weights, output.
MASK_W = [[1.0, 0.0, 0.0], [0.3302, 0.6698, 0.0], [0.2483, 0.2483, 0.5035]]

# ---------------------------------------------------------------- HAND: compounding (Week 10)
COMPOUND_BASE = 0.9526
COMPOUND_T = [1, 10, 20, 30, 40]
COMPOUND_VALS = [COMPOUND_BASE ** k for k in COMPOUND_T]        # 40 -> 0.143

# ---------------------------------------------------------------- LEDGER: BPE demo (Week 20)
BPE_MERGE1 = ("l", "o", "lo", 7)                      # (108, 111) -> 256, count 7
BPE_LOWEST = ("lowest", ["low", "e", "st"], [257, 101, 260])

# ---------------------------------------------------------------- HAND: cosine cards (Week 25)
COS_A, COS_B, COS_C = (1, 0, 3), (2, 0, 6), (4, 2, 0)
COS_TABLE = [[1.000, 1.000, 0.283], [1.000, 1.000, 0.283], [0.283, 0.283, 1.000]]

# ---------------------------------------------------------------- LEDGER: Week 26 recall (stranger set)
RECALL_LITERAL = (10, 10, 10)                         # hits at k=1,3,5 out of 10
RECALL_STRANGER = (2, 5, 6)
RECALL_K = (1, 3, 5)
RECALL_N = 10

# ---------------------------------------------------------------- LEDGER: Week 28 worked agent run
TRACE = [  # iteration, in tokens, out tokens, cost, tool, result
    (1, 247, 28, 0.000387, "search_notes", "ok"),
    (2, 415, 10, 0.000465, "calculate", "ok"),
    (3, 448, 25, 0.000573, "write_file", "ERR"),
    (4, 519, 19, 0.000614, "write_file", "ok"),
    (5, 566, 20, 0.000666, "(answer)", "stop"),
]
TRACE_SPEND = 0.002705

# ---------------------------------------------------------------- HAND: triangular sum
TRI_K = 10
TRI_SUM = TRI_K * (TRI_K + 1) // 2                    # 1 + ... + 10 = 55 (Week 29 pairing)

# ---------------------------------------------------------------- LEDGER: Week 31 LoRA + regression
LORA_TABLE = [  # category, n, before hits, after hits
    ("technical", 7, 2, 4),                           # 0.286 -> 0.571
    ("billing", 5, 2, 1),                             # 0.400 -> 0.200  (flagged)
]
LORA_OVERALL = (30, 18, 19)                           # n, base hits, LoRA hits
LORA_PARAMS = (2373, 123525)                          # trainable, all  (1.92 %)

# ---------------------------------------------------------------- HAND: LR schedule (AdamW 3e-4, warmup 100, 2500 steps)
LR_PEAK, LR_WARM, LR_TOTAL = 3e-4, 100, 2500


def lr_at(step):
    if step < LR_WARM:
        return LR_PEAK * step / LR_WARM
    return LR_PEAK * 0.5 * (1 + math.cos(math.pi * (step - LR_WARM) / (LR_TOTAL - LR_WARM)))


if __name__ == "__main__":
    for lr in DEMO_LRS:
        c = DEMO[lr]
        print("lr %-5s first %.3f last %.3f" % (lr, c[0], c[-1]))
    print("gap", GPT_GAP, "compound", [round(v, 3) for v in COMPOUND_VALS], "tri", TRI_SUM)
    print("peak lr at warmup end", lr_at(100), "end", lr_at(2500))

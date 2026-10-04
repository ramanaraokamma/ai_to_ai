import torch
import torch.nn.functional as F
torch.manual_seed(1)

FEATS = ["has_numbered_steps", "gives_direct_answer",
         "hedges_a_lot", "over_400_chars", "refuses"]

POOL = {                       # candidate responses as feature vectors
    "r1": [1, 1, 0, 0, 0],     # numbered steps, direct, concise
    "r2": [0, 1, 0, 0, 0],     # direct and concise, no structure
    "r3": [0, 1, 1, 1, 0],     # direct but hedgy and long
    "r4": [0, 0, 1, 0, 0],     # hedgy and evasive
    "r5": [0, 0, 0, 0, 1],     # refuses a harmless question
    "r6": [1, 1, 0, 1, 0],     # numbered steps, direct, but long
}

# Ten hand-made human judgements: (winner, loser)
PAIRS = [("r1", "r4"), ("r1", "r5"), ("r2", "r4"), ("r6", "r3"), ("r1", "r3"),
         ("r2", "r5"), ("r1", "r2"), ("r6", "r4"), ("r2", "r3"), ("r3", "r5")]

X = {k: torch.tensor(v, dtype=torch.float32) for k, v in POOL.items()}
w = torch.zeros(5, requires_grad=True)              # the reward model
opt = torch.optim.Adam([w], lr=0.1)

for step in range(1, 501):
    # Bradley-Terry: -log sigmoid( r(winner) - r(loser) )
    losses = [-F.logsigmoid(X[a] @ w - X[b] @ w) for a, b in PAIRS]
    loss = torch.stack(losses).mean()
    opt.zero_grad(); loss.backward(); opt.step()
    if step in (1, 100, 500):
        print(f"step {step:4d}  BT loss {loss.item():.4f}")

print("\nlearned reward weights:")
for f, wi in zip(FEATS, w.detach()):
    print(f"  {f:22s} {wi:+.3f}")

print("\nranking of every candidate:")
scores = {k: (X[k] @ w).item() for k in POOL}
for k, v in sorted(scores.items(), key=lambda kv: -kv[1]):
    print(f"  {k}  reward {v:+.3f}   {POOL[k]}")

agree = sum(scores[a] > scores[b] for a, b in PAIRS)
print(f"\ntrain-pair agreement: {agree}/{len(PAIRS)}")

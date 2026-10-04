import torch
import torch.nn.functional as F
torch.manual_seed(1)

FEATS = ["has_numbered_steps", "gives_direct_answer", "hedges_a_lot",
         "over_400_chars", "refuses", "is_factually_correct"]

POOL = {
    "r1": [1, 1, 0, 0, 0, 1],
    "r2": [0, 1, 0, 0, 0, 1],
    "r3": [0, 1, 1, 1, 0, 1],
    "r4": [0, 0, 1, 0, 0, 1],
    "r5": [0, 0, 0, 0, 1, 1],
    "r6": [1, 1, 0, 1, 0, 1],
    "r7": [1, 1, 0, 0, 0, 1],   # identical to r1 but CORRECT
    "r8": [1, 1, 0, 0, 0, 0],   # identical to r1 but WRONG
}
# Everything the raters actually compared happened to be factually correct,
# so r7/r8 never appear in any pair and the feature never varies within one.
PAIRS = [("r1", "r4"), ("r1", "r5"), ("r2", "r4"), ("r6", "r3"), ("r1", "r3"),
         ("r2", "r5"), ("r1", "r2"), ("r6", "r4"), ("r2", "r3"), ("r3", "r5")]

X = {k: torch.tensor(v, dtype=torch.float32) for k, v in POOL.items()}
w = torch.zeros(6, requires_grad=True)
opt = torch.optim.Adam([w], lr=0.1)
for _ in range(500):
    loss = torch.stack([-F.logsigmoid(X[a] @ w - X[b] @ w) for a, b in PAIRS]).mean()
    opt.zero_grad(); loss.backward(); opt.step()

for f, wi in zip(FEATS, w.detach()):
    print(f"  {f:22s} {wi:+.3f}")
print(f"\nr7 (correct)   reward {(X['r7'] @ w).item():+.3f}")
print(f"r8 (incorrect) reward {(X['r8'] @ w).item():+.3f}")

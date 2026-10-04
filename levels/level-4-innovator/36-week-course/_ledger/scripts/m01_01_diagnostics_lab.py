# LEDGER COPY of levels/level-4-innovator/module-01-deep-learning-at-depth.md (block 2,3,4,5 concatenated in document order). Module file is untouched.
"""Module 1 Hands-On: one dataset, one network, one knob at a time."""
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

DEVICE = "cpu"  # LEDGER: forced cpu (module picks cuda/mps)
print("device:", DEVICE)


# ---------------------------------------------------------------- 1. data
def make_spirals(n_per_class=600, noise=0.22, seed=0):
    """Two interleaved spirals. Hard enough that tuning actually matters."""
    rng = np.random.default_rng(seed)
    xs, ys = [], []
    for c in range(2):
        t = np.linspace(0.35, 3.4, n_per_class)      # radius grows along the arm
        theta = 2.1 * t + c * np.pi                  # class 1 is a half-turn behind
        x1 = t * np.cos(theta) + rng.normal(0, noise, n_per_class)
        x2 = t * np.sin(theta) + rng.normal(0, noise, n_per_class)
        xs.append(np.stack([x1, x2], axis=1))
        ys.append(np.full(n_per_class, c))
    X = np.concatenate(xs).astype(np.float32)
    y = np.concatenate(ys).astype(np.int64)
    p = rng.permutation(len(X))                      # shuffle before splitting
    return X[p], y[p]


X, y = make_spirals()
n_train = int(0.7 * len(X))
Xtr = torch.tensor(X[:n_train], device=DEVICE)
ytr = torch.tensor(y[:n_train], device=DEVICE)
Xva = torch.tensor(X[n_train:], device=DEVICE)
yva = torch.tensor(y[n_train:], device=DEVICE)

# Standardize using TRAIN statistics only. Using val stats here would be a leak.
mu, sd = Xtr.mean(0, keepdim=True), Xtr.std(0, keepdim=True)
Xtr = (Xtr - mu) / sd
Xva = (Xva - mu) / sd
print("train", tuple(Xtr.shape), "val", tuple(Xva.shape))


# ------------------------------------------------------------- 2. network
class Block(nn.Module):
    """Pre-norm block: norm -> linear -> activation -> dropout, optional residual."""
    def __init__(self, width, norm="none", dropout=0.0, residual=False):
        super().__init__()
        self.fc = nn.Linear(width, width)
        self.act = nn.GELU()
        self.drop = nn.Dropout(dropout)
        self.residual = residual
        if norm == "batch":
            self.norm = nn.BatchNorm1d(width)
        elif norm == "layer":
            self.norm = nn.LayerNorm(width)
        else:
            self.norm = nn.Identity()          # a no-op, so shapes stay identical

    def forward(self, x):
        h = self.drop(self.act(self.fc(self.norm(x))))
        return x + h if self.residual else h   # the gradient highway


class MLP(nn.Module):
    def __init__(self, width=64, depth=4, norm="none", dropout=0.0, residual=False):
        super().__init__()
        self.stem = nn.Linear(2, width)
        self.blocks = nn.Sequential(*[
            Block(width, norm, dropout, residual) for _ in range(depth)])
        self.head = nn.Linear(width, 2)

    def forward(self, x):
        return self.head(self.blocks(self.stem(x)))


# ------------------------------------------------------------ 3. one run
def run(tag, *, lr=3e-3, batch_size=64, epochs=60, optimizer="adamw",
        weight_decay=0.0, dropout=0.0, norm="none", residual=False,
        schedule="none", warmup_frac=0.0, clip=None, seed=0):
    torch.manual_seed(seed)                    # same init for every experiment
    model = MLP(norm=norm, dropout=dropout, residual=residual).to(DEVICE)

    if optimizer == "sgd":
        opt = torch.optim.SGD(model.parameters(), lr=lr, weight_decay=weight_decay)
    elif optimizer == "momentum":
        opt = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9,
                              weight_decay=weight_decay)
    elif optimizer == "adam":
        opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    else:
        opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)

    steps_per_epoch = max(1, len(Xtr) // batch_size)
    total_steps = steps_per_epoch * epochs
    warmup_steps = int(warmup_frac * total_steps)

    def lr_mult(step):
        """Returns a MULTIPLIER on the base lr, applied by LambdaLR."""
        if warmup_steps > 0 and step < warmup_steps:
            return (step + 1) / warmup_steps                     # linear ramp up
        if schedule == "cosine":
            prog = (step - warmup_steps) / max(1, total_steps - warmup_steps)
            return 0.5 * (1 + np.cos(np.pi * min(1.0, prog)))    # 1 -> 0 smoothly
        if schedule == "step":
            return 0.1 ** (step // max(1, total_steps // 3))     # /10 every third
        return 1.0                                               # constant lr

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_mult)
    lossf = nn.CrossEntropyLoss()
    hist = {"train": [], "val": [], "acc": [], "lr": [], "gnorm": []}
    g = torch.Generator(device="cpu").manual_seed(seed)

    for ep in range(epochs):
        model.train()                          # dropout ON, batchnorm uses batch stats
        perm = torch.randperm(len(Xtr), generator=g).to(DEVICE)
        running, nb = 0.0, 0
        for i in range(steps_per_epoch):
            idx = perm[i * batch_size:(i + 1) * batch_size]
            loss = lossf(model(Xtr[idx]), ytr[idx])
            opt.zero_grad(set_to_none=True)    # clear last step's gradients
            loss.backward()                    # accumulate this step's gradients
            gn = torch.nn.utils.clip_grad_norm_(   # returns the PRE-clip norm
                model.parameters(), clip if clip else float("inf"))
            opt.step()                         # apply the update
            sched.step()                       # advance the lr schedule
            running += loss.item()
            nb += 1

        model.eval()                           # dropout OFF, batchnorm uses running stats
        with torch.no_grad():
            vlogits = model(Xva)
            vloss = lossf(vlogits, yva).item()
            vacc = (vlogits.argmax(1) == yva).float().mean().item()

        hist["train"].append(running / nb)
        hist["val"].append(vloss)
        hist["acc"].append(vacc)
        hist["lr"].append(opt.param_groups[0]["lr"])
        hist["gnorm"].append(float(gn))

    print(f"{tag:<28} train {hist['train'][-1]:.3f}  "
          f"val {hist['val'][-1]:.3f}  acc {hist['acc'][-1]*100:5.1f}%")
    return hist


# --------------------------------------------------- 4. six controlled runs
results = {}
results["sgd lr=0.03"]            = run("sgd lr=0.03", optimizer="sgd", lr=0.03)
results["momentum lr=0.03"]       = run("momentum lr=0.03", optimizer="momentum", lr=0.03)
results["adamw lr=0.003"]         = run("adamw lr=0.003", lr=3e-3)
results["adamw lr=0.3 (too big)"] = run("adamw lr=0.3 (too big)", lr=0.3)
results["adamw + cosine"]         = run("adamw + cosine", schedule="cosine",
                                        warmup_frac=0.05)
results["adamw + ln + residual"]  = run("adamw + ln + res", norm="layer", residual=True)

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
for k, h in results.items():
    ax[0].plot(h["train"], label=k)
    ax[1].plot(h["val"], label=k)
ax[0].set_title("train loss")
ax[1].set_title("val loss")
for a in ax:
    a.set_xlabel("epoch"); a.set_ylabel("cross-entropy"); a.set_yscale("log")
ax[1].legend(fontsize=7)
plt.tight_layout()
plt.savefig("optimizer_comparison.png", dpi=110)
print("saved optimizer_comparison.png")

# ------------------------------------------- 5. deliberately overfit
X2, y2 = make_spirals(n_per_class=600, noise=0.35, seed=1)
n2 = int(0.7 * len(X2))
Xtr_full = torch.tensor(X2[:n2], device=DEVICE)
ytr_full = torch.tensor(y2[:n2], device=DEVICE)
mu2, sd2 = Xtr_full.mean(0, keepdim=True), Xtr_full.std(0, keepdim=True)

Xtr, ytr = ((Xtr_full - mu2) / sd2)[:120], ytr_full[:120]   # only 120 examples!
Xva = (torch.tensor(X2[n2:], device=DEVICE) - mu2) / sd2
yva = torch.tensor(y2[n2:], device=DEVICE)

over = {
    "no regularization": run("no regularization", epochs=250),
    "dropout 0.3":       run("dropout 0.3", epochs=250, dropout=0.3),
    "weight decay 0.3":  run("weight decay 0.3", epochs=250, weight_decay=0.3),
}
for name, h in over.items():
    best = int(np.argmin(h["val"]))
    print(f"{name:<20} best val {min(h['val']):.3f} @ epoch {best:>3}"
          f"   final val {h['val'][-1]:.3f}")

plt.figure(figsize=(7, 4.5))
for name, h in over.items():
    line, = plt.plot(h["val"], label=f"{name} (val)")
    plt.plot(h["train"], "--", color=line.get_color(), alpha=0.5)
plt.xlabel("epoch"); plt.ylabel("loss"); plt.legend(fontsize=8)
plt.title("solid = val, dashed = train")
plt.tight_layout(); plt.savefig("overfitting.png", dpi=110)

import copy

def run_with_early_stopping(patience=25, **kw):
    """Wrap run(): track the best val epoch and report what you would have kept."""
    h = run("early-stop probe", **kw)
    best_ep, best_val = int(np.argmin(h["val"])), float(min(h["val"]))
    # simulate the patience rule on the recorded history
    stop_ep = len(h["val"]) - 1
    for ep in range(len(h["val"])):
        if ep - int(np.argmin(h["val"][:ep + 1])) >= patience:
            stop_ep = ep
            break
    print(f"  would stop at epoch {stop_ep}, keeping weights from {best_ep} "
          f"(val {best_val:.3f}) instead of {h['val'][-1]:.3f}")
    return h

_ = run_with_early_stopping(patience=25, epochs=250)

import copy

def early_stopping_state():
    return {"best_val": float("inf"), "best_state": None, "bad_epochs": 0}


def early_stopping_update(st, model, vloss, patience=25, min_delta=1e-4):
    """Call once per epoch. Returns True when you should stop."""
    if vloss < st["best_val"] - min_delta:
        st["best_val"], st["bad_epochs"] = vloss, 0
        # deepcopy, or the saved tensors alias the live model and keep changing
        st["best_state"] = copy.deepcopy(model.state_dict())
        return False
    st["bad_epochs"] += 1
    return st["bad_epochs"] >= patience


# usage inside your epoch loop:
#     if early_stopping_update(st, model, vloss, patience=25):
#         break
# and after the loop:
#     model.load_state_dict(st["best_state"])

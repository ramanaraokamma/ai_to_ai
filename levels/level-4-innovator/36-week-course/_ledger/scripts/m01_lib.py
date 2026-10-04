# LEDGER: module 1 harness sections 1-3 only (no six-run demo), plus answer-key edit: depth kwarg (Practice 4) and LAST_MODEL hook.
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
def run(tag, *, depth=4, lr=3e-3, batch_size=64, epochs=60, optimizer="adamw",
        weight_decay=0.0, dropout=0.0, norm="none", residual=False,
        schedule="none", warmup_frac=0.0, clip=None, seed=0):
    torch.manual_seed(seed)                    # same init for every experiment
    model = MLP(depth=depth, norm=norm, dropout=dropout, residual=residual).to(DEVICE)

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
    globals()["LAST_MODEL"] = model   # LEDGER addition so answer-key probes can reach the model
    return hist



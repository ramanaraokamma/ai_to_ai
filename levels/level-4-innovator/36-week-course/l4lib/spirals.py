"""spirals.py - two interleaved spirals, plus the Module 1 training harness.

Used in weeks 1-7 (every Term 1 experiment) and week 19 (ablation harness reuse).

make_spirals(n, noise, seed) is numpy-only and fully seeded: same arguments, same
points, every time. `n` is points PER CLASS (600 -> 1,200 points -> 840 train / 360 val).

run(tag, *, lr, ..., depth=4) trains an MLP on the spirals, pinned to CPU, one seed
in, one history dict out. `depth` is shipped as an argument (not left as homework).
Data is built lazily on first use, so `import l4lib.spirals` is cheap and prints nothing.
"""
import numpy as np

DEVICE = "cpu"   # pinned on purpose: same numbers on every laptop


def make_spirals(n=600, noise=0.22, seed=0):
    """Two interleaved spirals. Returns X (2n, 2) float32 and y (2n,) int64, shuffled."""
    rng = np.random.default_rng(seed)
    xs, ys = [], []
    for c in range(2):
        t = np.linspace(0.35, 3.4, n)                # radius grows along the arm
        theta = 2.1 * t + c * np.pi                  # class 1 is a half-turn behind
        x1 = t * np.cos(theta) + rng.normal(0, noise, n)
        x2 = t * np.sin(theta) + rng.normal(0, noise, n)
        xs.append(np.stack([x1, x2], axis=1))
        ys.append(np.full(n, c))
    X = np.concatenate(xs).astype(np.float32)
    y = np.concatenate(ys).astype(np.int64)
    p = rng.permutation(len(X))                      # shuffle before splitting
    return X[p], y[p]


_DATA = {}


def get_data(n=600, noise=0.22, seed=0, train_frac=0.7):
    """Return (Xtr, ytr, Xva, yva) as torch tensors, standardized with TRAIN stats only."""
    import torch
    key = (n, noise, seed, train_frac)
    if key not in _DATA:
        X, y = make_spirals(n, noise, seed)
        k = int(train_frac * len(X))
        Xtr, ytr = torch.tensor(X[:k]), torch.tensor(y[:k])
        Xva, yva = torch.tensor(X[k:]), torch.tensor(y[k:])
        mu, sd = Xtr.mean(0, keepdim=True), Xtr.std(0, keepdim=True)   # train only: no leak
        _DATA[key] = ((Xtr - mu) / sd, ytr, (Xva - mu) / sd, yva)
    return _DATA[key]


def _nn():
    import torch.nn as nn

    class Block(nn.Module):
        """norm -> linear -> activation -> dropout, optional residual."""
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
                self.norm = nn.Identity()

        def forward(self, x):
            h = self.drop(self.act(self.fc(self.norm(x))))
            return x + h if self.residual else h

    class MLP(nn.Module):
        def __init__(self, width=64, depth=4, norm="none", dropout=0.0, residual=False):
            super().__init__()
            self.stem = nn.Linear(2, width)
            self.blocks = nn.Sequential(*[
                Block(width, norm, dropout, residual) for _ in range(depth)])
            self.head = nn.Linear(width, 2)

        def forward(self, x):
            return self.head(self.blocks(self.stem(x)))

    return Block, MLP


def make_model(width=64, depth=4, norm="none", dropout=0.0, residual=False):
    """Build the Module 1 MLP (stem, `depth` blocks, head)."""
    _, MLP = _nn()
    return MLP(width=width, depth=depth, norm=norm, dropout=dropout, residual=residual)


def run(tag, *, depth=4, lr=3e-3, batch_size=64, epochs=60, optimizer="adamw",
        weight_decay=0.0, dropout=0.0, norm="none", residual=False,
        schedule="none", warmup_frac=0.0, clip=None, seed=0, verbose=True):
    """Train one model; return a history dict (train, val, acc, lr, gnorm per epoch)."""
    import torch
    import torch.nn as nn
    Xtr, ytr, Xva, yva = get_data()
    torch.manual_seed(seed)                    # same init for every experiment
    model = make_model(depth=depth, norm=norm, dropout=dropout, residual=residual)

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
        """A MULTIPLIER on the base lr, applied by LambdaLR."""
        if warmup_steps > 0 and step < warmup_steps:
            return (step + 1) / warmup_steps
        if schedule == "cosine":
            prog = (step - warmup_steps) / max(1, total_steps - warmup_steps)
            return 0.5 * (1 + np.cos(np.pi * min(1.0, prog)))
        if schedule == "step":
            return 0.1 ** (step // max(1, total_steps // 3))
        return 1.0

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_mult)
    lossf = nn.CrossEntropyLoss()
    hist = {"train": [], "val": [], "acc": [], "lr": [], "gnorm": []}
    g = torch.Generator(device="cpu").manual_seed(seed)

    for ep in range(epochs):
        model.train()
        perm = torch.randperm(len(Xtr), generator=g)
        running, nb = 0.0, 0
        for i in range(steps_per_epoch):
            idx = perm[i * batch_size:(i + 1) * batch_size]
            loss = lossf(model(Xtr[idx]), ytr[idx])
            opt.zero_grad(set_to_none=True)
            loss.backward()
            gn = torch.nn.utils.clip_grad_norm_(      # returns the PRE-clip norm
                model.parameters(), clip if clip else float("inf"))
            opt.step()
            sched.step()
            running += loss.item()
            nb += 1

        model.eval()
        with torch.no_grad():
            vlogits = model(Xva)
            vloss = lossf(vlogits, yva).item()
            vacc = (vlogits.argmax(1) == yva).float().mean().item()

        hist["train"].append(running / nb)
        hist["val"].append(vloss)
        hist["acc"].append(vacc)
        hist["lr"].append(opt.param_groups[0]["lr"])
        hist["gnorm"].append(float(gn))

    if verbose:
        print(f"{tag:<28} train {hist['train'][-1]:.3f}  "
              f"val {hist['val'][-1]:.3f}  acc {hist['acc'][-1]*100:5.1f}%")
    return hist

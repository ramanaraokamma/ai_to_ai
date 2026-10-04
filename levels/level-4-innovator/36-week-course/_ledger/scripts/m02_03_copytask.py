import sys, time
from m02_lib import *
def make_copy_batch(B=64, L=5, D=10, n_sym=8, seed=None):
    if seed is not None:
        torch.manual_seed(seed)
    core = torch.randint(0, n_sym, (B, L))
    filler = torch.full((B, D), n_sym)
    return torch.cat([core, filler, core], dim=1), core


def run_copy(cell, D, L=5, n_sym=8, steps=1500, hidden=64):
    torch.manual_seed(0)
    vocab = n_sym + 1
    m = CharRNN(vocab, emb=16, hidden=hidden, cell=cell, p_drop=0.0)
    opt = torch.optim.AdamW(m.parameters(), lr=3e-3)
    for step in range(steps):
        seq, core = make_copy_batch(64, L, D, n_sym)
        inp = torch.cat([torch.full((64, 1), n_sym), seq[:, :-1]], dim=1)
        logits, _ = m(inp)
        # only score the final L positions -- the copied part
        loss = F.cross_entropy(logits[:, -L:].reshape(-1, vocab),
                               core.reshape(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
    with torch.no_grad():
        seq, core = make_copy_batch(512, L, D, n_sym, seed=99)
        inp = torch.cat([torch.full((512, 1), n_sym), seq[:, :-1]], dim=1)
        logits, _ = m(inp)
        acc = (logits[:, -L:].argmax(-1) == core).float().mean().item()
    return acc



cell=sys.argv[1]
for D in [1, 5, 10, 20, 40]:
    t0=time.time()
    print(cell, D, f"{run_copy(cell, D):.3f}", f"({time.time()-t0:.0f}s)", flush=True)

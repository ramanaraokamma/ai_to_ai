from m03_train import *
import time
def sinusoidal(max_len, d):
    pe = torch.zeros(max_len, d)
    pos = torch.arange(max_len).unsqueeze(1).float()
    div = torch.exp(torch.arange(0, d, 2).float() * (-math.log(10000.0) / d))
    pe[:, 0::2] = torch.sin(pos * div)
    pe[:, 1::2] = torch.cos(pos * div)
    return pe

class SinGPT(TinyGPT):
    def __init__(self, vocab, **kw):
        super().__init__(vocab, **kw)
        del self.pos_emb
        self.register_buffer("pe", sinusoidal(4096, self.tok_emb.embedding_dim))

    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pe[:T].to(idx.device)
        for b in self.blocks:
            x = b(x)
        logits = self.head(self.ln_f(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                   targets.reshape(-1))
        return logits, loss
BLK=32
import m03_lib
m03_lib.BLOCK=BLK   # get_batch reads the module global BLOCK
globals()["BLOCK"]=BLK
import m03_lib as _l
_l.BLOCK=BLK
results={}
for kind in ("learned","sinusoidal"):
    torch.manual_seed(1337)
    model=(TinyGPT(V,block=BLK) if kind=="learned" else SinGPT(V,block=BLK)).to(DEVICE)
    print("training",kind,"BLOCK=32", flush=True)
    best,lo,sec=fit(model,1500)
    print(f"  {kind}: best val {best[0]:.3f} @ {best[1]}  final val {lo['val']:.3f} ({sec:.0f}s)", flush=True)
    results[kind]=model
@torch.no_grad()
def eval_len(model,L,fix_mask=False):
    model.eval()
    if fix_mask:   # LEDGER: enlarge the causal-mask buffers so L > 32 does not shape-error
        for b in model.blocks:
            for h in b.attn.heads: h.tril=torch.tril(torch.ones(L,L))
    torch.manual_seed(0); ls=[]
    d=val_data
    for _ in range(20):
        ix=torch.randint(len(d)-L-1,(BATCH,))
        x=torch.stack([d[i:i+L] for i in ix]); y=torch.stack([d[i+1:i+L+1] for i in ix])
        ls.append(model(x,y)[1].item())
    return sum(ls)/len(ls)
for kind,model in results.items():
    for L in (32,48,64):
        try: print(f"{kind:10s} eval length {L}: val loss {eval_len(model,L):.3f}")
        except Exception as e: print(f"{kind:10s} eval length {L}: {type(e).__name__}: {str(e)[:110]}")
print("--- with causal-mask buffer enlarged to L (ledger fix, not in module) ---")
for kind,model in results.items():
    for L in (48,64):
        try: print(f"{kind:10s} eval length {L}: val loss {eval_len(model,L,fix_mask=True):.3f}")
        except Exception as e: print(f"{kind:10s} eval length {L}: {type(e).__name__}: {str(e)[:110]}")

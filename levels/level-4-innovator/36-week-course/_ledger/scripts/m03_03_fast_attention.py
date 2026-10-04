import time
from m03_lib import *
class MultiHeadAttentionFast(nn.Module):
    def __init__(self, n_embd, n_head, block, dropout):
        super().__init__()
        assert n_embd % n_head == 0
        self.n_head, self.n_embd = n_head, n_embd
        self.qkv = nn.Linear(n_embd, 3 * n_embd, bias=False)
        self.proj = nn.Linear(n_embd, n_embd)
        self.attn_drop = nn.Dropout(dropout)
        self.resid_drop = nn.Dropout(dropout)
        self.register_buffer("tril", torch.tril(torch.ones(block, block))
                                          .view(1, 1, block, block))

    def forward(self, x):
        B, T, C = x.shape
        hs = C // self.n_head
        q, k, v = self.qkv(x).split(C, dim=2)                    # 3 x (B,T,C)
        q = q.view(B, T, self.n_head, hs).transpose(1, 2)        # (B,nh,T,hs)
        k = k.view(B, T, self.n_head, hs).transpose(1, 2)
        v = v.view(B, T, self.n_head, hs).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) * hs ** -0.5             # (B,nh,T,T)
        att = att.masked_fill(self.tril[:, :, :T, :T] == 0, float("-inf"))
        att = self.attn_drop(F.softmax(att, dim=-1))
        y = att @ v                                              # (B,nh,T,hs)
        y = y.transpose(1, 2).contiguous().view(B, T, C)         # re-merge heads
        return self.resid_drop(self.proj(y))
torch.manual_seed(0)
slow = MultiHeadAttention(128, 4, 64, 0.0).eval()
fast = MultiHeadAttentionFast(128, 4, 64, 0.0).eval()
with torch.no_grad():
    qw = torch.cat([h.query.weight for h in slow.heads], dim=0)   # (128,128)
    kw = torch.cat([h.key.weight   for h in slow.heads], dim=0)
    vw = torch.cat([h.value.weight for h in slow.heads], dim=0)
    fast.qkv.weight.copy_(torch.cat([qw, kw, vw], dim=0))         # (384,128)
    fast.proj.weight.copy_(slow.proj.weight)
    fast.proj.bias.copy_(slow.proj.bias)

x = torch.randn(2, 40, 128)
with torch.no_grad():
    a, b = slow(x), fast(x)
print("max abs diff:", (a - b).abs().max().item())
assert torch.allclose(a, b, atol=1e-5)
print("equivalent")

# timing (Practice 4 text: warm up once, 100 forward passes on randn(32,64,128))
xx=torch.randn(32,64,128)
with torch.no_grad():
    slow(xx); fast(xx)
    t0=time.perf_counter()
    for _ in range(100): slow(xx)
    ts=time.perf_counter()-t0
    t0=time.perf_counter()
    for _ in range(100): fast(xx)
    tf=time.perf_counter()-t0
print(f"100 fwd: loop {ts:.3f}s  batched {tf:.3f}s  speedup {ts/tf:.2f}x")

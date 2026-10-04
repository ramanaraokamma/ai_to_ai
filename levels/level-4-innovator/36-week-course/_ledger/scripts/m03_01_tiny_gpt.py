# LEDGER COPY of module-03 block 4 (tiny_gpt.py), DEVICE forced cpu; one line appended at the end to save weights for the probes.
"""Module 3 Hands-On — a character-level GPT, built from scratch."""
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

torch.manual_seed(1337)
DEVICE = "cpu"  # LEDGER: forced cpu (module picks cuda/mps)

# ------------------------------------------------------------------ 1. data
CORPUS = """
the sun rose over the quiet town and the baker opened her door.
the baker made bread every morning before the sun rose.
the boy walked to school with a book under his arm.
the girl walked to school with a kite under her arm.
the teacher asked a question and the class went quiet.
a question is a small door and an answer is a room behind it.
the river ran past the town and the town grew beside the river.
in the morning the river was quiet and in the evening it was loud.
the old man fed the birds by the river every single morning.
the birds knew the old man and the old man knew the birds.
a bridge crossed the river and the children crossed the bridge.
under the bridge the water was cold and dark and slow.
the market opened at noon and closed when the sun went down.
at the market you could buy bread and fish and rope and salt.
the fisherman sold fish and the baker sold bread and both were happy.
the rope maker made rope and nobody asked how the rope was made.
a cat slept on the wall beside the market every afternoon.
the cat did not care about bread or fish or rope or salt.
the cat cared about the sun on the wall and nothing else.
when it rained the market closed and the cat found a dry door.
the rain fell on the roofs and ran down into the river.
the river rose and the bridge held and the town slept.
in the winter the river froze and the children walked on it.
the old man told them not to walk on the river in the winter.
the children listened to the old man because the old man was right.
a story is a road and a road goes somewhere if you follow it.
the teacher said that a question is better than a guess.
the boy said that a guess is better than nothing at all.
the girl said that both of them were right and both were wrong.
the class laughed and the teacher wrote the question on the board.
every morning the baker counted her loaves before she opened.
every evening the fisherman counted his fish before he went home.
counting is a quiet thing and it makes the world hold still.
the old man did not count the birds because the birds moved too much.
the sun rose over the quiet town and the day began again.
a town is a machine made of people and roads and small kindnesses.
the baker gave bread to the old man and the old man fed the birds.
the birds sang over the river and the children heard them sing.
the teacher opened a window so the class could hear the birds.
a window is a door for sound and light but not for people.
the boy drew a bird in his book and the girl drew a river.
the teacher drew a bridge between the bird and the river.
that is how a lesson works said the teacher and the class went quiet.
in the spring the ice broke and the river ran fast and brown.
the fisherman waited because the fish would come back in time.
waiting is work even when it does not look like work.
the rope maker made a long rope and gave it to the fisherman.
the fisherman tied his boat to the bridge with the long rope.
the boat held and the river ran and the town went on.
the cat watched the boat from the wall and did not move.
the sun went down behind the roofs and the market closed.
the baker swept her floor and the teacher closed her window.
the old man walked home along the river in the last of the light.
the children ran ahead of him and he did not try to keep up.
a town at night is a quiet machine and it still runs.
in the morning the baker opened her door before the sun rose.
the boy asked the old man why the birds came back every year.
the old man said that the birds remember the shape of the river.
the girl asked whether a river has a shape at all.
the old man said that everything has a shape if you watch it long enough.
the teacher wrote the word shape on the board and drew a river beside it.
the class copied the word and nobody copied the river.
the boy copied the river and left the word out.
the teacher said that both of those are notes and neither one is wrong.
a note is a rope you throw to the person you will be tomorrow.
the rope maker liked that line and asked the teacher to write it down.
the teacher wrote it on a small card and gave it to the rope maker.
the rope maker kept the card in his pocket for the rest of the winter.
the fisherman found a broken oar under the bridge one cold morning.
he carried the oar to the rope maker and the rope maker mended it.
mending is quieter than making and it is often harder.
the baker mended a torn sack with thread and did not tell anyone.
the teacher mended a broken chair and told the whole class about it.
the old man mended nothing because the old man threw nothing away.
the cat mended nothing and the cat was not ashamed.
in the summer the market stayed open until the light was gone.
the children ran between the stalls and nobody stopped them.
the fisherman gave a small fish to the cat and the cat took it.
the cat did not thank the fisherman because cats do not do that.
the fisherman did not mind because he had not asked for thanks.
a gift with a price on it is a trade and both of them are fine.
the baker traded bread for fish and the fisherman traded fish for bread.
the rope maker traded rope for both and everyone went home full.
the teacher traded questions for answers and the class grew.
the old man traded nothing and the town gave him bread anyway.
in the autumn the leaves fell into the river and floated to the sea.
the boy asked where the sea was and the girl said far past the bridge.
the old man said the sea is where the river stops explaining itself.
the teacher wrote that on the board and did not explain it.
the class thought about it for a long time and then went home.
some questions are meant to be carried and not answered.
the boy carried that one all winter and asked about it in the spring.
the old man had forgotten saying it and laughed a long time.
the girl remembered every word and told him what he had said.
the old man said that is why we need more than one person in a town.
the baker heard the story and put it in her bread song.
she sang the bread song every morning while the loaves rose.
the loaves did not care about the song but the baker did.
a song is a way of counting that does not feel like counting.
the fisherman sang nothing and counted his fish in his head.
the rope maker hummed and lost count and started over every time.
the teacher sang badly and the class loved her for it.
the children sang the bread song walking home over the bridge.
the old man heard them from the river and fed the birds and smiled.
the birds did not sing back because the birds were eating.
in the last week of winter the ice broke with a sound like a door.
the whole town heard it and everybody knew what it meant.
the fisherman untied his boat and the rope maker checked the rope.
the baker made extra bread and the teacher opened the window.
the old man walked to the bridge and watched the brown water go.
the children came running and the cat stayed on the wall.
the sun rose over the quiet town and the day began again.
"""

text = CORPUS.strip()
chars = sorted(set(text))              # every distinct character, sorted
V = len(chars)                         # vocabulary size
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join(itos[i] for i in l)

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]
print(f"{len(text)} chars | vocab {V} | train {len(train_data)} "
      f"val {len(val_data)} | device {DEVICE}")

BLOCK = 64        # context length: how far back the model can see
BATCH = 32
N_EMBD = 128      # d_model
N_HEAD = 4        # so each head gets 128/4 = 32 dimensions
N_LAYER = 4
DROPOUT = 0.1


def get_batch(split):
    """Grab BATCH random windows of length BLOCK; y is x shifted one right."""
    d = train_data if split == "train" else val_data
    ix = torch.randint(len(d) - BLOCK - 1, (BATCH,))
    x = torch.stack([d[i:i + BLOCK] for i in ix])
    y = torch.stack([d[i + 1:i + BLOCK + 1] for i in ix])
    return x.to(DEVICE), y.to(DEVICE)


# --------------------------------------------------------- 2. one attention head
class Head(nn.Module):
    def __init__(self, n_embd, head_size, block, dropout):
        super().__init__()
        # no bias: the bias would be absorbed by layer norm anyway
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        # a buffer moves with .to(device) but is not a trainable parameter
        self.register_buffer("tril", torch.tril(torch.ones(block, block)))
        self.drop = nn.Dropout(dropout)
        self.last_attn = None                       # stashed for the heatmap

    def forward(self, x):
        B, T, C = x.shape
        k, q, v = self.key(x), self.query(x), self.value(x)   # each (B,T,hs)
        # (B,T,hs) @ (B,hs,T) -> (B,T,T);  the *hs**-0.5 is the 1/sqrt(d_k) scaling
        att = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5
        att = att.masked_fill(self.tril[:T, :T] == 0, float("-inf"))  # causal
        att = F.softmax(att, dim=-1)                # rows now sum to 1
        self.last_attn = att.detach()
        return self.drop(att) @ v                   # (B,T,T) @ (B,T,hs) -> (B,T,hs)


# ------------------------------------------------------ 3. multi-head attention
class MultiHeadAttention(nn.Module):
    def __init__(self, n_embd, n_head, block, dropout):
        super().__init__()
        hs = n_embd // n_head                       # 128 // 4 = 32
        self.heads = nn.ModuleList([Head(n_embd, hs, block, dropout)
                                    for _ in range(n_head)])
        self.proj = nn.Linear(n_embd, n_embd)       # W_O: blends the heads
        self.drop = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)   # (B,T,n_embd)
        return self.drop(self.proj(out))


# ------------------------------------------------------------ 4. the MLP
class FeedForward(nn.Module):
    """Applied to each position independently. Attention gathers, this thinks."""
    def __init__(self, n_embd, dropout):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd), nn.GELU(),
            nn.Linear(4 * n_embd, n_embd), nn.Dropout(dropout))

    def forward(self, x):
        return self.net(x)


# --------------------------------------------------- 5. the transformer block
class Block(nn.Module):
    def __init__(self, n_embd, n_head, block, dropout):
        super().__init__()
        self.ln1 = nn.LayerNorm(n_embd)
        self.attn = MultiHeadAttention(n_embd, n_head, block, dropout)
        self.ln2 = nn.LayerNorm(n_embd)
        self.ff = FeedForward(n_embd, dropout)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))   # pre-norm + residual (Module 1)
        x = x + self.ff(self.ln2(x))
        return x


# --------------------------------------------------------------- 6. the GPT
class TinyGPT(nn.Module):
    def __init__(self, vocab, n_embd=N_EMBD, n_head=N_HEAD, n_layer=N_LAYER,
                 block=BLOCK, dropout=DROPOUT):
        super().__init__()
        self.block_size = block
        self.tok_emb = nn.Embedding(vocab, n_embd)   # what the token is
        self.pos_emb = nn.Embedding(block, n_embd)   # where the token is
        self.blocks = nn.ModuleList([Block(n_embd, n_head, block, dropout)
                                     for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)             # final norm before the head
        self.head = nn.Linear(n_embd, vocab)         # project to vocab logits
        self.apply(self._init)

    def _init(self, m):
        """GPT-2's initialization: small normal weights, zero biases."""
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.tok_emb(idx) + self.pos_emb(pos)    # token + position
        for b in self.blocks:
            x = b(x)
        logits = self.head(self.ln_f(x))             # (B, T, vocab)
        loss = None
        if targets is not None:
            # every one of the T positions is a training example
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                   targets.reshape(-1))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0, top_k=None):
        """Autoregressive sampling — Module 2's loop, new engine."""
        self.eval()
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size:]     # never exceed the context
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / temperature  # only the last position
            if top_k is not None:
                v = torch.topk(logits, top_k).values
                logits[logits < v[:, [-1]]] = -float("inf")
            probs = F.softmax(logits, dim=-1)
            idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
        self.train()
        return idx


model = TinyGPT(V).to(DEVICE)
print(f"parameters: {sum(p.numel() for p in model.parameters()):,}")

# ------------------------------------------------------------- 7. training
opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
MAX_STEPS = 2500
WARMUP = 100
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (      # Module 1
    (s + 1) / WARMUP if s < WARMUP else
    0.5 * (1 + math.cos(math.pi * (s - WARMUP) / (MAX_STEPS - WARMUP)))))


@torch.no_grad()
def estimate_loss(iters=20):
    """Average over several batches — a single batch is far too noisy."""
    model.eval()
    out = {}
    for split in ["train", "val"]:
        losses = torch.zeros(iters)
        for k in range(iters):
            x, y = get_batch(split)
            _, l = model(x, y)
            losses[k] = l.item()
        out[split] = losses.mean().item()
    model.train()
    return out


history = []
CHECKPOINTS = [0, 300, 1200, 2499]
for step in range(MAX_STEPS):
    if step in CHECKPOINTS:                      # watch it learn
        ctx = torch.tensor([[stoi["t"]]], device=DEVICE)
        torch.manual_seed(0)
        s = decode(model.generate(ctx, 220, temperature=0.8)[0].tolist())
        lo = estimate_loss()
        print(f"\n--- step {step} | train {lo['train']:.3f} "
              f"val {lo['val']:.3f} ---")
        print(repr(s))
    x, y = get_batch("train")
    _, loss = model(x, y)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    sched.step()
    history.append(loss.item())
    if step % 500 == 0:
        lo = estimate_loss()
        print(f"step {step:4d} train {lo['train']:.3f} val {lo['val']:.3f}")

lo = estimate_loss()
print(f"\nFINAL train {lo['train']:.3f} val {lo['val']:.3f}")
ctx = torch.tensor([[stoi["t"]]], device=DEVICE)
torch.manual_seed(0)
print(decode(model.generate(ctx, 400, temperature=0.8)[0].tolist()))

# ------------------------------------------------- 8. look inside the heads
prompt = "the baker made bread every morning"
idx = torch.tensor([encode(prompt)], device=DEVICE)
model.eval()
with torch.no_grad():
    model(idx)                                   # populates every last_attn

print("\n=== what does each head look at? ===")
for li in range(N_LAYER):
    for hi in range(N_HEAD):
        a = model.blocks[li].attn.heads[hi].last_attn[0]      # (T, T)
        T = a.shape[0]
        pos = torch.arange(T, device=a.device).float()
        dist = ((pos.unsqueeze(0) - pos.unsqueeze(1)).abs() * a).sum(-1)
        print(f"L{li} H{hi}: mean look-back {dist[5:].mean():.2f} chars, "
              f"self-weight {a.diagonal().mean().item():.2f}")

q = len(prompt) - 1
a = model.blocks[1].attn.heads[0].last_attn[0][q]
top = torch.topk(a, 5)
print(f"\nquery = last char {prompt[q]!r} (pos {q}), top-5 attended:")
for w, i in zip(top.values.tolist(), top.indices.tolist()):
    print(f"   pos {i:2d} {prompt[i]!r}  weight {w:.3f}")

att = model.blocks[1].attn.heads[0].last_attn[0].cpu().numpy()
plt.figure(figsize=(7, 6))
plt.imshow(att, cmap="viridis")
plt.xticks(range(len(prompt)), list(prompt), fontsize=6)
plt.yticks(range(len(prompt)), list(prompt), fontsize=6)
plt.xlabel("key position (attended TO)")
plt.ylabel("query position (attending FROM)")
plt.colorbar(); plt.title("layer 1, head 0 — causal attention")
plt.tight_layout(); plt.savefig("attention_heatmap.png", dpi=110)

plt.figure(figsize=(7, 4))
plt.plot(history, alpha=0.3, label="per-step")
k = 50
plt.plot(np.arange(k - 1, len(history)),
         np.convolve(history, np.ones(k) / k, mode="valid"),
         label="50-step moving average")
plt.xlabel("step"); plt.ylabel("train loss"); plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("loss_curve.png", dpi=110)
print("\nsaved attention_heatmap.png and loss_curve.png")

# LEDGER addition
torch.save(model.state_dict(), "tiny_gpt_m03.pt")

# LEDGER COPY of module-02 block 3 (name_generator.py), unmodified except this header.
"""Module 2 Hands-On — char-level name generator + the vanishing-gradient probe."""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

torch.manual_seed(0)

# ------------------------------------------------------------------ 1. data
NAMES = """
aarav aditi adrian agnes ahmed aiko alina amara amelia anders andrei
anika anita ansel arjun armin arnav asha aslan astrid aurora
bashir beatrix bela bhavya bianca bjorn bodhi bruno cadence caleb
carla carmen cedric celia chandra chitra cira clara colette dagmar
dalia damian daria deepak delia devika dilan divya dmitri dorian
edith eleni elias elina elodie emil enzo esha eshan esme
fabio farah farhan felix fiona flora franka freya gabor gauri
gemma georgi gita greta gustav hana harini harsha havel heidi
helena hugo ilya imran indira ingrid irina iris isolde ivar
jaden jarek jasmin jatin javier jelena jonas joris juno kaia
kalinda karim kasper katya kavya kiran klara koen lakshmi lars
latika leena lena leonie liana linnea lucia lucas magnus maja
malik manav maren marek marisol matteo mila mira nadia nandini
natan nikhil niko nina noor nuria olen olga omkar oorja
orla oskar pablo paloma pavel petra pooja pranav priya quintus
rachna radek rafael rahul rasmus rekha renata rhea rosa rustam
saga sameer sanjay sanna sasha selma senna serge sigrid simone
sofia stefan svea tamara tanvi tarek tatiana thea tibor tomas
torsten trisha uday ujwal ulla ulrich uma vadim valeria varsha
veda vera viggo vikram vilma wanda willem yamini yara yash
ylva yuri zaid zara zenon zoltan zora zuri alma bex
cato dara eero fenna gero hilde ilma jarl kajsa lior
nael oona pim risto suvi timo urho vito wren xanthe
""".split()

PAD, EOS = 0, 1                       # id 0 = padding, id 1 = end-of-name
chars = sorted(set("".join(NAMES)))   # the 26 letters that actually occur
stoi = {c: i + 2 for i, c in enumerate(chars)}   # ids 2..27
itos = {i: c for c, i in stoi.items()}
V = len(stoi) + 2                     # vocabulary size including PAD and EOS
MAXLEN = max(len(n) for n in NAMES) + 1          # +1 leaves room for EOS
TRAIN_SET = set(NAMES)                # used later to measure novelty
print(f"{len(NAMES)} names | vocab {V} | max length with EOS {MAXLEN}")


def encode(name):
    """'aarav' -> [2, 2, 19, 2, 23, 1, 0, 0]  (letters, EOS, then padding)."""
    ids = [stoi[c] for c in name] + [EOS]
    return ids + [PAD] * (MAXLEN - len(ids))


data = torch.tensor([encode(n) for n in NAMES], dtype=torch.long)
# Teacher forcing: input at step t is the TRUE token from step t-1.
inputs = torch.full((len(NAMES), MAXLEN), PAD, dtype=torch.long)
inputs[:, 1:] = data[:, :-1]          # shift right; column 0 stays PAD = <START>
targets = data
print("inputs", tuple(inputs.shape), "targets", tuple(targets.shape))
print("example:", NAMES[0], "->", encode(NAMES[0]))


# --------------------------------------------------------------- 2. model
class CharRNN(nn.Module):
    def __init__(self, vocab, emb=24, hidden=64, cell="lstm", p_drop=0.3):
        super().__init__()
        self.emb = nn.Embedding(vocab, emb)
        self.hidden, self.cell_type = hidden, cell
        if cell == "rnn":
            self.cell = nn.RNNCell(emb, hidden, nonlinearity="tanh")
        elif cell == "gru":
            self.cell = nn.GRUCell(emb, hidden)
        elif cell == "lstm":
            self.cell = nn.LSTMCell(emb, hidden)
        else:
            raise ValueError(cell)
        self.drop = nn.Dropout(p_drop)      # regularization, from Module 1
        self.out = nn.Linear(hidden, vocab)

    def init_state(self, B):
        """LSTM carries (h, c); RNN and GRU carry only h."""
        h = torch.zeros(B, self.hidden)
        return (h, torch.zeros(B, self.hidden)) if self.cell_type == "lstm" else h

    def step(self, tok, state):
        """ONE time step. Used by the generation loop."""
        h_or_pair = self.cell(self.emb(tok), state)
        h = h_or_pair[0] if self.cell_type == "lstm" else h_or_pair
        return self.out(self.drop(h)), h_or_pair

    def forward(self, x, keep_hidden=False):
        """Whole sequence with teacher forcing. keep_hidden is for the probe."""
        B, T = x.shape
        state, logits, kept = self.init_state(B), [], []
        for t in range(T):                       # the unrolled loop
            state = self.cell(self.emb(x[:, t]), state)
            h = state[0] if self.cell_type == "lstm" else state
            if keep_hidden:
                h.retain_grad()                  # so we can read h.grad later
                kept.append(h)
            logits.append(self.out(self.drop(h)))
        return torch.stack(logits, 1), kept      # (B, T, V)


def train(cell="lstm", steps=800, lr=3e-3, wd=0.1, clip=1.0, verbose=True):
    torch.manual_seed(0)
    m = CharRNN(V, cell=cell)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=wd)
    losses = []
    for step in range(steps):
        m.train()
        logits, _ = m(inputs)                                # full batch: 231 names
        loss = F.cross_entropy(logits.reshape(-1, V), targets.reshape(-1),
                               ignore_index=PAD)             # padding must not count
        opt.zero_grad(set_to_none=True)
        loss.backward()
        gn = nn.utils.clip_grad_norm_(m.parameters(), clip)  # RNNs need this
        opt.step()
        losses.append(loss.item())
        if verbose and (step % 200 == 0 or step == steps - 1):
            print(f"  {cell:4s} step {step:4d}  loss {loss.item():.3f}  "
                  f"grad-norm {gn:.2f}")
    return m, losses


@torch.no_grad()
def sample(m, n=10, temperature=1.0, top_k=None, seed=0):
    """Autoregressive generation: the model's own output feeds the next step."""
    m.eval()                                     # turns dropout OFF (Module 1!)
    torch.manual_seed(seed)
    names = []
    for _ in range(n):
        state, tok, chs = m.init_state(1), torch.tensor([PAD]), []
        for _ in range(MAXLEN):
            logits, state = m.step(tok, state)
            logits = logits[0].clone()
            logits[PAD] = -1e9                   # never emit padding
            logits = logits / max(temperature, 1e-6)
            if top_k is not None:
                kth = torch.topk(logits, top_k).values[-1]
                logits[logits < kth] = -1e9      # everything outside top-k dies
            tok = torch.multinomial(F.softmax(logits, -1), 1).view(1)
            if tok.item() == EOS:
                break
            chs.append(itos[tok.item()])
        names.append("".join(chs))
    return names


print("\n=== training a plain RNN ===")
rnn, rnn_losses = train("rnn")
print("\n=== training an LSTM ===")
lstm, lstm_losses = train("lstm")

print("\n=== sampling from the LSTM ===")
for T in [0.5, 0.8, 1.2]:
    s = sample(lstm, 10, temperature=T, seed=1)
    novel = sum(x not in TRAIN_SET for x in s)
    print(f"T={T}: {novel}/10 novel  {s}")
s = sample(lstm, 10, temperature=1.0, top_k=5, seed=1)
print(f"top_k=5: {sum(x not in TRAIN_SET for x in s)}/10 novel  {s}")
for T in [0.5, 0.8, 1.0, 1.2]:
    s = sample(lstm, 60, temperature=T, seed=1)
    print(f"  novelty rate at T={T}: {sum(x not in TRAIN_SET for x in s)}/60")


# ------------------------------------------------- 3. vanishing gradients
def grad_by_position(cell="rnn", T=40, w_scale=1.0, forget_bias=None, seed=0):
    """Measure ||dLoss_T / dh_t|| for every t. Untrained net, random input."""
    torch.manual_seed(seed)
    m = CharRNN(V, hidden=96, cell=cell, p_drop=0.0)
    with torch.no_grad():
        if w_scale != 1.0:
            m.cell.weight_hh.mul_(w_scale)       # crank up to force explosion
        if forget_bias is not None:
            H = m.hidden
            # PyTorch LSTMCell bias layout is [input, forget, cell, output]
            m.cell.bias_ih[H:2 * H].fill_(forget_bias)
            m.cell.bias_hh[H:2 * H].fill_(0.0)
    x = torch.randint(2, V, (1, T))
    logits, kept = m(x, keep_hidden=True)
    F.cross_entropy(logits[:, -1], torch.tensor([2])).backward()  # loss at LAST step
    return [h.grad.norm().item() for h in kept]


probes = {
    "RNN (default init)":        grad_by_position("rnn"),
    "RNN (W_hh x 8, exploding)": grad_by_position("rnn", w_scale=8.0),
    "LSTM (default init)":       grad_by_position("lstm"),
    "LSTM (forget bias = +2)":   grad_by_position("lstm", forget_bias=2.0),
    "GRU (default init)":        grad_by_position("gru"),
}
print("\n=== ||dL_40/dh_t|| ===")
for k, g in probes.items():
    print(f"{k:28s} t=40 {g[-1]:.2e} | t=20 {g[19]:.2e} | t=1 {g[0]:.2e}"
          f" | ratio {g[0]/g[-1]:.2e}")

plt.figure(figsize=(8, 4.8))
for k, g in probes.items():
    plt.plot(range(1, len(g) + 1), g, marker="o", ms=3, label=k)
plt.yscale("log"); plt.xlabel("time step t"); plt.ylabel("|| dLoss_40 / dh_t ||")
plt.title("How far back does the learning signal reach?")
plt.legend(fontsize=8); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig("vanishing_gradients.png", dpi=110)

plt.figure(figsize=(7, 4))
plt.plot(rnn_losses, label="RNN"); plt.plot(lstm_losses, label="LSTM")
plt.xlabel("step"); plt.ylabel("cross-entropy"); plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("rnn_vs_lstm_loss.png", dpi=110)
print("saved plots")

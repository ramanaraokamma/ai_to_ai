from m02_lib import *
class MyLSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size, forget_bias=0.0):
        super().__init__()
        self.hidden_size = hidden_size
        # one linear for all four gates: [i, f, g, o] stacked, matching PyTorch
        self.x2h = nn.Linear(input_size, 4 * hidden_size)
        self.h2h = nn.Linear(hidden_size, 4 * hidden_size)
        with torch.no_grad():
            H = hidden_size
            self.x2h.bias[H:2 * H].fill_(forget_bias)
            self.h2h.bias[H:2 * H].fill_(0.0)

    def forward(self, x, state):
        h_prev, c_prev = state
        gates = self.x2h(x) + self.h2h(h_prev)          # (B, 4H)
        i, f, g, o = gates.chunk(4, dim=1)              # PyTorch's ifgo order
        i, f, o = torch.sigmoid(i), torch.sigmoid(f), torch.sigmoid(o)
        g = torch.tanh(g)
        c = f * c_prev + i * g                          # the additive highway
        h = o * torch.tanh(c)
        return h, c


# ---- equivalence test against nn.LSTMCell ----
torch.manual_seed(0)
ref = nn.LSTMCell(16, 32)
mine = MyLSTMCell(16, 32)
with torch.no_grad():
    mine.x2h.weight.copy_(ref.weight_ih)
    mine.h2h.weight.copy_(ref.weight_hh)
    mine.x2h.bias.copy_(ref.bias_ih)
    mine.h2h.bias.copy_(ref.bias_hh)

x = torch.randn(4, 16)
s = (torch.zeros(4, 32), torch.zeros(4, 32))
hr, cr = ref(x, s)
hm, cm = mine(x, s)
print("max |h diff| =", (hr - hm).abs().max().item())
print("max |c diff| =", (cr - cm).abs().max().item())
assert torch.allclose(hr, hm, atol=1e-5) and torch.allclose(cr, cm, atol=1e-5)
print("equivalence OK")

print("\n=== forget-bias sweep (Practice 5), untrained 96-unit LSTM, T=40 ===")
for fb in [0, 1, 2, 4]:
    g = grad_by_position("lstm", forget_bias=float(fb))
    print(f"forget_bias={fb}  sigma={torch.sigmoid(torch.tensor(float(fb))).item():.3f}  grad t=40 {g[-1]:.2e}  t=20 {g[19]:.2e}  t=1 {g[0]:.2e}  ratio {g[0]/g[-1]:.2e}")

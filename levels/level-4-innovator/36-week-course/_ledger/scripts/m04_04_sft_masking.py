import torch
import torch.nn.functional as F
torch.manual_seed(0)

V = 12                                    # pretend vocabulary size
logits = torch.randn(1, 9, V)             # pretend model output for 9 positions
tokens = torch.tensor([[3, 7, 2, 9, 11, 4, 4, 1, 6]])
PROMPT_LEN = 5                            # first 5 tokens are the prompt

preds = logits[:, :-1, :]                 # position t predicts token t+1
targets_all = tokens[:, 1:].clone()

loss_all = F.cross_entropy(preds.reshape(-1, V), targets_all.reshape(-1))

targets_sft = targets_all.clone()
targets_sft[:, :PROMPT_LEN - 1] = -100    # -100 == "ignore me"
loss_sft = F.cross_entropy(preds.reshape(-1, V),
                           targets_sft.reshape(-1), ignore_index=-100)

print("targets_all:", targets_all.tolist())
print("targets_sft:", targets_sft.tolist())
print(f"loss over all 8 predictions   : {loss_all.item():.4f}")
print(f"loss over 4 response positions: {loss_sft.item():.4f}")

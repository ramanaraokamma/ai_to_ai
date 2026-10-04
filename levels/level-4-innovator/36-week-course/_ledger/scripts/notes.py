NOTEBOOK = """# Lab Notebook — AI Academy Level 4

## 2026-01-14 — Optimizer bake-off
Ran SGD, SGD+momentum and AdamW on the same 3-layer MLP. Plain SGD needed 40 epochs
to reach the loss AdamW hit in 6. Momentum 0.9 closed most of the gap. Conclusion:
start with AdamW, and only reach for tuned SGD+momentum if AdamW plateaus early.

## 2026-01-21 — Learning rate sweep
Swept lr over 1e-1, 1e-2, 1e-3, 1e-4. At 1e-1 the loss shot up to NaN by step 30.
At 1e-4 the curve was smooth but still falling at the end of training. 1e-3 was best.
Warmup over the first 200 steps removed the early spike entirely.

## 2026-02-03 — Dropout and weight decay
Dropout 0.1 changed almost nothing. Dropout 0.5 hurt training loss badly and only
helped validation on the smallest dataset. Weight decay 0.01 in AdamW gave a steadier
validation curve than dropout did. Note: AdamW decouples weight decay from the
gradient, which is why it behaves differently from L2 added to the loss.

## 2026-02-18 — Character RNN on names
Trained a char-level RNN on 900 typed-in names. Sampling at temperature 0.5 gave
boring but pronounceable output. Temperature 1.2 gave unpronounceable junk. 0.8 was
the sweet spot. Gradient magnitude at position 1 was 3e-12 of the value at position 40.

## 2026-03-02 — LSTM vs GRU
The GRU trained slightly faster per epoch and reached the same loss as the LSTM.
Both were far better than the plain RNN at holding information across 30 steps.
Gradient decay was about 0.95 per step instead of 0.6 per step.

## 2026-03-19 — Attention by hand
Worked scaled dot-product attention for a 3-token sequence on paper. Without the
1/sqrt(d_k) scaling the softmax saturated and one weight became 0.997. With scaling
the weights were 0.52, 0.31, 0.17. Scaling matters more as d_k grows.

## 2026-04-05 — Tiny GPT training run
Four layers, four heads, 128 embedding dim, block size 64. Trained on 1.1 MB of text
for 5000 steps. Validation loss went 4.21 -> 1.68. Samples were readable English by
step 3000. Attention head L0H2 mostly looked at the previous character.

## 2026-04-22 — Positional encodings
Swapped learned positional embeddings for sinusoidal ones. Almost no difference on
this size of model. Removing positional information entirely raised validation loss
from 1.68 to 2.41, which confirms the model really is permutation-blind without it.

## 2026-05-08 — Batch size experiment
Batch 16 vs batch 128 at the same learning rate. The large batch had a much smoother
loss curve and slightly worse final validation loss. Scaling lr by 2x for the large
batch recovered most of the difference. Gradient noise seems to act as a regularizer.

## 2026-05-20 — Layer norm placement
Pre-norm (norm before attention) trained stably without warmup. Post-norm needed
warmup or it diverged in the first 100 steps. Went with pre-norm everywhere.

## 2026-06-11 — BPE tokenizer from scratch
Implemented byte-level BPE. On a 1117-byte corpus it learned 138 merges before every
remaining pair became unique. Compression was 2.22 bytes per token versus about 4.5
for GPT-2. Round-trip on emoji and Devanagari passed once I switched from characters
to bytes.

## 2026-06-25 — Reward model toy
Fitted a linear Bradley-Terry reward model to 10 hand-made comparisons. It learned
+5.05 for numbered steps and exactly 0.00 for factual correctness, because no pair
in the data differed only in correctness. Cheapest way to raise reward: number things.

## 2026-07-09 — DPO on a four-option policy
Ran DPO with beta 0.2 for 300 steps. The policy collapsed to a single option with
probability 0.997. With contradictory preference pairs the two contradicted options
reverted exactly to the reference model's own ratio. Loss floor for a perfect cycle
is log 2 = 0.6931.

## 2026-07-28 — Prompt bench
Twenty extraction test cases, four prompt versions. Zero-shot 59.4%, rules 78.1%,
few-shot 90.6%. The constant-answer baseline was 43.8%, which reframed everything.
Adaptive thinking cost 6.8x more and scored 3 points lower on this task.

## 2026-08-14 — Cost accounting
One extraction call is about 420 input and 60 output tokens. At 2 dollars per million
input and 10 per million output that is 0.00144 dollars per call. A full eval run of
80 calls costs about 12 cents. Output tokens are five times the price of input tokens.
"""


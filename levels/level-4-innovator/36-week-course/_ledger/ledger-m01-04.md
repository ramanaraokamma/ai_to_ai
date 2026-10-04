# Ground-truth ledger, modules 1-4

Real CPU runs of every runnable Python block in `module-01` to `module-04`. Nothing here is invented: each number below was printed by a script in `scripts/`, and the full stdout (with a `WALL_SECONDS` footer) is in `out/<script>.txt`. The modules were not edited.

## How this was run

- torch 2.2.1, CPU only, `MPLBACKEND=Agg`, `PYTHONHASHSEED=0`, `OMP_NUM_THREADS=2`, stdin closed. No network, no transformers, no torchvision.
- **Seeds.** Each module's own seeds were kept, because the module text's numbers depend on them: M1 seed 0, M2 seed 0, M3 `manual_seed(1337)`, M4 0 / 1. Nothing was re-seeded to 0 that the module seeds differently. Repeat runs of `m01_02_answerkey.py` (three times) and `m03_03_fast_attention.py` gave identical numerics (only timings vary); other scripts were run once.
- **cuda/mps to cpu.** Only M1 and M3 select a device. The copies in `scripts/` have that assignment replaced with `DEVICE = "cpu"`. M2 and M4 have no device code.
- **Timing.** Wall seconds for the whole process. Scripts `m03_04_sinusoidal` and `m03_05_ablate *` ran 9-at-a-time on 2 threads each, so their seconds are inflated (roughly 2-3x); the single-run reference is `m03_01` (133 s for 2,500 steps). Nothing exceeded 5 minutes, so **no reduced-step variant was needed** except where the module itself specifies fewer steps (the mask-break probe is 500 steps, as the answer key says).
- **Ledger additions (not in the modules, each marked `LEDGER` in the script).** `seed=` parameter on M2 `train()` (default 0 = identical behaviour); `depth=` on M1 `run()` and a `LAST_MODEL` hook (both prescribed/implied by the M1 answer key); a tiny harness that trains then evaluates on shifted data (M1 Practice 6B, text gives no code); `model.state_dict()` saved after the M3 run so head probes need not retrain; ablation/sinusoidal/mask-break training loops for M3 (text gives only a comment or model class). Ablations use the module's optimiser (AdamW 3e-4, wd 0.1, 100 warmup, cosine) with the cosine horizon set to the run length, and track best validation loss every 50 steps.

## Headline findings (where the module text is wrong on real CPU runs)

1. **M1 numbers all drift.** Only `sgd lr=0.03` (0.690 / 0.690 / 52.8%) and the "too big" accuracy (46.9%) match. Every other printed line differs, and the module's overfitting story is ordered differently (section 1.2).
2. **M1 Practice answer-key verdicts do not reproduce.** `lr=1e-4` is healthy (98.1%), not underfit (~85%). Batch 128/256 at lr 1e-3 are *not* worse than batch 32 (0.033 / 0.028 vs 0.056), so "linear scaling breaks at 256" does not show up. `dropout=0.8` is not underfit (val 0.182, 93.6%). Grad-norm "doesn't decay for lr=0.3" is false (229 to 0.077). Depth-12 plain net trains fine (98.9%). **Layer norm does not survive the +1.5 shift** (acc 48.3%, same failure as batch norm 46.7%), contradicting "layer norm recomputes per example and adapts".
3. **M2 main script reproduces exactly**, including `3.28e-12`, `9.38e+06`, loss curves and samples. Weak spots are the answer-key claims: the copy task (RNN falls to chance at D=5, LSTM at D=20, not "D=10-20" / "often to D=40"), and `0.95^400 = 1.23e-9`, not `4e-9`.
4. **M3 main script matches structurally** (807,196 parameters, 6972 chars, overfit U-curve) but every loss and sample differs slightly, and the ablation table is largely wrong: 1 head and 1 layer are *not* worse (1.269 / 1.271 vs 1.278); removing the sqrt(d_k) scaling gave the *best* val of all (1.245); removing residuals is 2.848, worse than the module's 2.3; batched attention is **slower** than the loop on CPU (0.78-0.81x), not 2-4x faster. **The sinusoidal model crashes at length 48/64 as written** (causal-mask buffer is 32x32), so the module's 1.55 / 1.68 cannot be produced without an extra fix, and with that fix the losses are 1.87 / 2.22.
5. **M4 reproduces to the last digit** (BPE 138 merges / 760 tokens / 1.47, reward weights, DPO sweeps, SFT masking 3.8008 / 4.0407). Only hand-arithmetic rounding differs in the 4th decimal. Everything using the gpt2 tokenizer was skipped.

---

## Module 1 (`module-01-deep-learning-at-depth.md`)

Python blocks: 14 (block 1 is a one-line `clip_grad_norm_` snippet, not standalone; blocks 2-5 are the lab; 6-14 are answer-key code). Scripts: `m01_01_diagnostics_lab.py` (blocks 2,3,4,5 concatenated in document order, as the text says "add this at the bottom"), `m01_02_answerkey.py` (blocks 6-14 with `m01_lib.py` = sections 1-3 of block 2), `m01_03_practice2_overfit400.py`.

### 1.1 `m01_01_diagnostics_lab.py` - 3.9 s

```
device: cpu
train (840, 2) val (360, 2)
sgd lr=0.03                  train 0.690  val 0.690  acc  52.8%
momentum lr=0.03             train 0.018  val 0.034  acc  98.6%
adamw lr=0.003               train 0.007  val 0.037  acc  98.9%
adamw lr=0.3 (too big)       train 0.701  val 0.723  acc  46.9%
adamw + cosine               train 0.007  val 0.045  acc  98.9%
adamw + ln + res             train 0.011  val 0.022  acc  99.4%
no regularization            train 0.023  val 0.495  acc  93.3%
dropout 0.3                  train 0.127  val 0.355  acc  93.6%
weight decay 0.3             train 0.047  val 0.269  acc  92.5%
no regularization    best val 0.199 @ epoch  85   final val 0.495
dropout 0.3          best val 0.199 @ epoch 177   final val 0.355
weight decay 0.3     best val 0.174 @ epoch 161   final val 0.269
  would stop at epoch 110, keeping weights from 85 (val 0.199) instead of 0.495
```

Differs from module text?

| Module text (printed/claimed) | Real CPU | Verdict |
|---|---|---|
| `device: mps` | `device: cpu` | expected |
| `train (840, 2) val (360, 2)` | same | match |
| sgd 0.690 / 0.690 / 52.8% | 0.690 / 0.690 / 52.8% | **match** |
| momentum 0.013 / 0.098 / 98.9% | 0.018 / 0.034 / 98.6% | differs (val 0.098 vs 0.034) |
| adamw 3e-3 0.005 / 0.035 / 99.2% | 0.007 / 0.037 / 98.9% | differs |
| adamw lr=0.3 0.701 / 0.724 / 46.9% | 0.701 / 0.723 / 46.9% | val differs by 0.001; acc match |
| cosine 0.004 / 0.039 / 99.2% | 0.007 / 0.045 / 98.9% | differs |
| ln+res 0.006 / 0.034 / 99.2% | 0.011 / 0.022 / 99.4% | differs |
| no-reg 0.013 / 0.591 / 91.7% | 0.023 / 0.495 / 93.3% | differs |
| dropout 0.3: 0.090 / 0.413 / 90.0% | 0.127 / 0.355 / 93.6% | differs |
| wd 0.3: 0.002 / 0.408 / 92.8% | 0.047 / 0.269 / 92.5% | differs |
| no-reg best 0.216 @ 41, final 0.591 | best 0.199 @ 85, final 0.495 | differs (epoch 41 vs 85) |
| dropout best 0.209 @ 67, final 0.413 | 0.199 @ 177, 0.355 | differs |
| wd best 0.219 @ 42, final 0.408 | 0.174 @ 161, 0.269 | differs |
| "all three reach almost the same best val (~0.21)" | 0.199 / 0.199 / 0.174 | roughly true; wd clearly best (0.174) |
| "final loss 0.591 vs 0.413 vs 0.408" (dropout ~ wd) | 0.495 vs 0.355 vs 0.269 | ordering holds; dropout and wd no longer tied |
| "Early stopping at epoch 41 beats every regularizer" (0.216 < 0.413) | epoch 85, 0.199 < 0.355 and < 0.269 | **claim still holds, epoch number changes** |
| early-stop probe (no printed number in text) | stops at epoch 110, keeps epoch 85 (0.199) vs 0.495 | new ground truth |
| "ln(2) = 0.693, sgd pinned at 0.69" | 0.690 | match |

### 1.2 `m01_02_answerkey.py` - 19.5 s (blocks 6-14; sections timed inside the file)

```
adamw lr=1e-05               train 0.683  val 0.679  acc  55.3%
adamw lr=0.0001              train 0.077  val 0.063  acc  98.1%
adamw lr=0.001               train 0.018  val 0.026  acc  99.4%
adamw lr=0.01                train 0.013  val 0.059  acc  99.2%
adamw lr=0.1                 train 0.693  val 0.702  acc  46.9%
-- Practice 2 configs --
lr=1e-6                      train 0.693  val 0.692  acc  53.1%
lr=0.5                       train 0.648  val 0.712  acc  46.9%
dropout=0.8                  train 0.376  val 0.182  acc  93.6%
lr=3e-3 epochs=5             train 0.133  val 0.145  acc  95.0%
-- Practice 3 scaling (60 epochs) --
bs=32  lr=0.001  val 0.056   bs=64 lr=0.001 val 0.026   bs=64 lr=0.002 val 0.058
bs=128 lr=0.001  val 0.033   bs=128 lr=0.004 val 0.050
bs=256 lr=0.001  val 0.028   bs=256 lr=0.008 val 0.031
-- fixed steps --
bs=32 val 0.041   bs=64 val 0.026   bs=128 val 0.070   bs=256 val 0.044
-- Practice 4 --
gnorm first/last epoch  lr=3e-3 : 0.168 -> 0.026 (max 3.126)
gnorm first/last epoch  lr=0.3  : 229.16 -> 0.077 (max 229.16)
depth12 plain: gnorm 0.0742 -> 0.9505, train 0.695 -> 0.031, acc 98.9%
depth12 res  : gnorm 0.4654 -> 0.032,  train 0.772 -> 0.010, acc 98.9%
block[0].fc.weight grad norm (depth12 res, end of training): 0.01262
-- Practice 5 LR range test --
loss minimum at lr=1.29e-02  ->  suggested lr=1.29e-03
suggested 1.29e-3            train 0.012  val 0.049  acc  98.9%
default 3e-3                 train 0.007  val 0.037  acc  98.9%
-- Practice 6A (batch size 2, 30 epochs) --
bn bs=2                      train 0.688  val 0.677  acc  56.4%
ln bs=2                      train 0.105  val 0.034  acc  98.6%
-- Practice 6B (2x2, val shifted by +1.5) --
batch norm  matched: loss 0.019 acc 99.4%   shifted: loss 4.480 acc 46.7%
layer norm  matched: loss 0.064 acc 98.9%   shifted: loss 4.523 acc 48.3%
```

Also `m01_03_practice2_overfit400.py` (1.2 s): 120 examples, 400 epochs: train 0.009, val 0.525, acc 92.5%, best val 0.199 @ epoch 85.

Differs from module text?

| Module text | Real CPU | Verdict |
|---|---|---|
| lr 1e-5: ~0.69 / ~0.69 / ~50%, "(C) dead flat at ln 2" | 0.683 / 0.679 / 55.3% | approx; slightly moving |
| lr 1e-4: ~0.35 / ~0.36 / ~85% "(E) underfitting" | 0.077 / 0.063 / 98.1% | **wrong**: healthy |
| lr 1e-3: ~0.02 / ~0.05 / ~99% | 0.018 / 0.026 / 99.4% | ok (val lower) |
| lr 1e-2: ~0.02 / ~0.09 / ~98% "noisier" | 0.013 / 0.059 / 99.2% | approx |
| lr 1e-1: ~0.69 / ~0.71 / ~50% | 0.693 / 0.702 / 46.9% | ok |
| "lr=0.3 is worse still (0.701)" | 0.701 val 0.723 (lab run) | match |
| lr=1e-6 flat 0.693 | 0.693 / 0.692 / 53.1% | match |
| lr=0.5 "loss around/above 0.69" | train 0.648 val 0.712 / 46.9% | ok |
| dropout=0.8 "(E) both plateau 0.4-0.6" | train 0.376, val **0.182**, 93.6% | **wrong**: not underfit; val < train |
| 400 epochs/120 ex: val bottoms ~epoch 40, "climbs past 0.6" | best 0.199 @ 85, final 0.525 | differs (epoch, and never past 0.6) |
| lr=3e-3, epochs=5: "both 0.3-0.5, still falling" | 0.133 / 0.145 / 95.0% | differs (much better) |
| "780 steps" at bs 64, 60 epochs | 13 x 60 = 780 | match |
| "about 195 vs 1560 steps" (bs 256 vs 32) | 3 x 60 = 180 vs 26 x 60 = 1560 | 195 wrong (180 real) |
| scaling table ~0.04 / 0.05 / 0.04 / 0.09 / 0.04 / 0.18 / 0.05 | 0.056 / 0.026 / 0.058 / 0.033 / 0.050 / 0.028 / 0.031 | **does not reproduce**; no large-batch degradation |
| "linear scaling breaks at 256" | 256 at 1e-3 (0.028) beats 32 (0.056) | **not supported** on this task |
| lr=0.3 gnorm "10-1000x larger and does not decay" | 229 vs 0.17 at epoch 0 (about 1,360x), but falls to 0.077 | first half true; "does not decay" false |
| depth-12 plain "far smaller gnorm, stalls" | 0.074 first epoch, but rises to 0.95 and trains to 98.9% | **wrong** on stalling |
| depth-12 residual "same order as 4-block" | 0.465 first epoch, 0.032 last (4-block: 0.168 / 0.026) | ok |
| LR range: min near 1e-2 to 3e-2; suggested 1e-3 to 3e-3 | 1.29e-2; 1.29e-3 | match |
| suggested vs default "which wins" (no numbers) | default 3e-3 val 0.037 beats suggested 0.049 | new ground truth |
| bn bs=2 fails, ln bs=2 fine | bn 0.677 / 56.4%, ln 0.034 / 98.6% | match |
| "layer norm recomputes per example and adapts" to shift | LN shifted 4.523 / 48.3% (same failure as BN 4.480 / 46.7%) | **wrong** here; the shift enters before any norm layer |

---

## Module 2 (`module-02-sequence-models.md`)

Python blocks: 9 (block 1 snippet; 2 pseudo-code; 3 the full script; 4 copy-task stub; 5 train(seed) fragment; 6 seed loop; 7 copy task; 8 MyLSTMCell; 9 exposure bias). Scripts: `m02_01_name_generator.py` (verbatim block 3), `m02_02_seeds_rnn_gru_lstm.py`, `m02_03_copytask.py rnn|lstm`, `m02_04_mylstm_and_forgetbias.py`, `m02_05_exposure_bias.py`, `m02_06_handcalc_checks.py`; all share `m02_lib.py` (block 3 sections 1-2 plus `grad_by_position`).

### 2.1 `m02_01_name_generator.py` - 5.1 s

Printed output is **character-for-character identical to the module's Expected output**: `231 names | vocab 28 | max length with EOS 8`, loss trajectories (rnn 3.370 / 1.653 / 1.343 / 1.201 / 1.167; lstm 3.345 / 1.596 / 1.153 / 1.052 / 1.026), grad norms, all sample lists (`dira`, `tieo`, `arjav`, `chelaa`), novelty 0 / 6 / 12 / 18 of 60, and the probe:

```
RNN (default init)           t=40 5.45e-01 | t=20 6.54e-07 | t=1 3.28e-12 | ratio 6.01e-12
RNN (W_hh x 8, exploding)    t=40 5.69e-01 | t=20 2.19e+03 | t=1 9.38e+06 | ratio 1.65e+07
LSTM (default init)          t=40 6.29e-01 | t=20 1.41e-05 | t=1 6.69e-09 | ratio 1.06e-08
LSTM (forget bias = +2)      t=40 6.24e-01 | t=20 2.16e-02 | t=1 1.60e-02 | ratio 2.56e-02
GRU (default init)           t=40 5.48e-01 | t=20 2.36e-05 | t=1 4.55e-09 | ratio 8.31e-09
```

| Module text | Real CPU | Verdict |
|---|---|---|
| `3.28e-12` (t=1, RNN) | 3.28e-12 | **match** |
| `9.38e+06` (t=1, W_hh x 8) | 9.38e+06 | **match** |
| ratio 6.01e-12 / 1.65e+07 / 1.06e-08 / 2.56e-02 / 8.31e-09 | identical | match |
| LSTM ends 1.026, RNN 1.167; RNN grad-norm 0.23 to 0.40, LSTM 0.16 to 0.12 | 1.026, 1.167; 0.23 to 0.40; 0.16 to 0.12 (final 0.15) | match (LSTM final gn 0.15, module says 0.12 at step 600) |
| "only 39x smaller than t=40" (forget bias +2) | 0.624/0.0160 = 39.0 | match |
| novelty 0 / 6 / 12 / 18 of 60 | same | match |
| "0.95^400 ~ 4 x 10^-9" (Common Mistakes, Key Takeaways) | 1.23e-9 (computed, `m02_06`) | **wrong by 3x** |
| "0.982^40 = 0.485" | 0.4836 | ok (rounding) |
| "3.28 x 10^-12 ... one four-hundred-billionth" (M3 intro) | 3.28e-12 | ok |

### 2.2 `m02_02_seeds_rnn_gru_lstm.py` - 17.2 s (9 trainings)

```
rnn   loss 1.176 (spread 0.022)  novel 27.3/60
gru   loss 1.036 (spread 0.014)  novel 10.0/60
lstm  loss 1.024 (spread 0.006)  novel 11.3/60
```

| Module text (approximate) | Real | Verdict |
|---|---|---|
| rnn ~1.17, spread ~0.03, novelty ~20 | 1.176, 0.022, 27.3 | loss ok; novelty differs (27 vs 20) |
| gru ~1.05, ~0.03, ~14 | 1.036, 0.014, 10.0 | differs modestly |
| lstm ~1.03, ~0.02, ~12 | 1.024, 0.006, 11.3 | ok |
| LSTM beats RNN by ~0.14, "~5x the spread (0.03)" | gap 0.152 = 7x the RNN spread (0.022) | direction right |
| LSTM vs GRU gap ~0.02 "same size as spread" | gap 0.012; spreads 0.006 / 0.014 | roughly true |
| "RNN fits worse so more novel" | 27.3 vs 10.0 / 11.3 | true |

### 2.3 `m02_03_copytask.py` - rnn 12.5 s, lstm 24.6 s (1500 steps per point, hidden 64, chance = 1/8 = 0.125)

```
rnn  D=1 1.000   D=5 0.438   D=10 0.129   D=20 0.127   D=40 0.127
lstm D=1 0.998   D=5 0.996   D=10 0.984   D=20 0.130   D=40 0.130
```

| Module text | Real | Verdict |
|---|---|---|
| both near 100% at D=1 | 1.000 / 0.998 | match |
| RNN drops below 50% "around D=10-20" | already 0.438 at D=5, chance by D=10 | earlier than claimed |
| LSTM "holds high accuracy ... often to D=40" | 0.984 at D=10, **chance (0.130) at D=20 and D=40** | **wrong at 1500 steps** |

### 2.4 `m02_04_mylstm_and_forgetbias.py` - 0.8 s

```
max |h diff| = 0.0   max |c diff| = 0.0   equivalence OK
forget_bias=0 sigma=0.500 t=1 3.99e-09   forget_bias=1 sigma=0.731 t=1 2.13e-04
forget_bias=2 sigma=0.881 t=1 1.60e-02   forget_bias=4 sigma=0.982 t=1 1.18e-01
(t=40 = 6.26e-01 to 6.29e-01 throughout)
```

Module: diffs "approximately 0.0 (under 1e-7)" match; table ~7e-09 / ~1e-04 / ~1.6e-02 / ~1.2e-01 vs real 3.99e-09 / 2.13e-04 / 1.60e-02 / 1.18e-01. The bias-0 figure differs from the module's 7e-09 (and from the 6.69e-09 of the default-init LSTM in 2.1, because `bias_hh` is zeroed here). Module says bias 4 ratio "within a factor of 2": real ratio 0.188 (about 5x).

### 2.5 `m02_05_exposure_bias.py` - 4.0 s

```
real names   mean 0.954  median 0.936  n=231
generated    mean 1.122  median 0.958  n=200
gap = 0.167 nats/char
```

Module: real "0.9-1.1" (match); generated "typically 1.2-1.6" (real 1.122, **below** that range; the median is almost equal to the real names, the gap comes from a right tail).

### 2.6 `m02_06_handcalc_checks.py` - 0.6 s (hand arithmetic from the answer key)

GRU: z = 0.7311 / 0.2689 / 0.2689; h~ = 0.9051 / 0.3193 / 0.2774; h = 0.6617 / **0.5696** / **0.4910** (module 0.5697 / 0.4911, rounding of intermediate steps). Softmax T=0.5 [0.867, 0.117, 0.016] match; T=1 [0.665, 0.245, 0.090] match; T=4 [0.419, **0.326**, 0.254] (module 0.327). Top-k=2 [0.731, 0.269, 0]. Vocabulary table: T=0.5 top prob 0.579 to 0.831, top-k [0.731, 0.269] all match.

---

## Module 3 (`module-03-attention-and-transformers.md`)

Python blocks: 9 (1 dict demo, 2-3 snippets, 4 the Tiny GPT, 5 ablation comment only, 6 fast MHA, 7 equivalence test, 8 sinusoidal, 9 head_stats). Scripts: `m03_01_tiny_gpt.py` (block 4; saves `out/run_m01_04/tiny_gpt_m03.pt`), `m03_02_headstats.py`, `m03_03_fast_attention.py`, `m03_04_sinusoidal.py`, `m03_05_ablate.py <name>`; `m03_lib.py`, `m03_train.py` helpers.

### 3.1 `m03_01_tiny_gpt.py` - 133.0 s (2,500 steps; the module says "roughly 2 minutes")

```
6972 chars | vocab 28 | train 6274 val 698 | device cpu
parameters: 807,196
--- step 0 | train 3.346 val 3.339 ---
step    0 train 3.340 val 3.335
--- step 300 | train 1.722 val 1.779 ---
step  500 train 1.226 val 1.410
step 1000 train 0.445 val 1.328
--- step 1200 | train 0.301 val 1.451 ---
step 1500 train 0.212 val 1.589
step 2000 train 0.159 val 1.664
--- step 2499 | train 0.148 val 1.682 ---
FINAL train 0.150 val 1.669
```

| Module text | Real CPU | Verdict |
|---|---|---|
| 6972 chars, vocab 28, 6274 / 698 | same | match |
| 807,196 parameters | 807,196 | **match** |
| step 0: train 3.346 val 3.340; step-0 line 3.340 / 3.334 | 3.346 / 3.339; 3.340 / 3.335 | within 0.001 |
| step 300: 1.705 / 1.761 | 1.722 / 1.779 | differs |
| step 500: 1.206 / 1.372 | 1.226 / 1.410 | differs |
| step 1000: 0.437 / 1.369 | 0.445 / 1.328 | differs |
| step 1200: 0.303 / 1.425 | 0.301 / 1.451 | differs |
| step 1500: 0.202 / 1.490 | 0.212 / 1.589 | differs |
| step 2000: 0.154 / 1.617 | 0.159 / 1.664 | differs |
| step 2499: 0.150 / 1.657 | 0.148 / 1.682 | differs |
| FINAL 0.146 / 1.644 | 0.150 / 1.669 | differs |
| val series "3.340 to 1.761 to 1.369 to 1.425 to 1.617 to 1.657", best near step 1000 | 3.339, 1.779, 1.328, 1.451, 1.664, 1.682; best near step 1000 | shape holds, numbers differ |
| "ln(28) = 3.332", step 0 "within a hair" | 3.346 / 3.339 | ok |
| step-0 sample `'t ouk.kugkaacystoyd...'` | `'tur.gah\nczcw\nqkhooe...'` | samples differ (illustrative in module) |
| step 300 / 1200 / 2499 samples | differ textually; step 1200 and 2499 are real-word text, 2499 is a verbatim corpus quote | qualitative claim holds |

Head statistics in the main script:

| Module text | Real |
|---|---|
| L0 H0 look-back 3.95, self 0.15 | 3.67, 0.15 |
| L0 H1 3.81, 0.15 | 3.72, 0.14 |
| L3 H2 8.69, 0.15 | 8.41, 0.15 |
| L3 H3 8.11, 0.11 | 7.59, 0.10 |
| layer means 3.66 / 6.94 / 7.26 / 8.26 ("monotonic") | 3.64 / 6.75 / 7.21 / 7.35 | monotonic still holds; L3 is 7.35 not 8.26 |
| top-5 for `g` (pos 33): 28 `o` 0.150, 29 `r` 0.101, 31 `i` 0.093, 26 space 0.081, 17 `e` 0.053 | 28 `o` 0.204, 29 `r` 0.162, 31 `i` 0.156, 33 `g` 0.076, 26 space 0.062 | same leading positions; weights and tail differ |

### 3.2 `m03_02_headstats.py` - 0.9 s (loads the model trained in 3.1; sentence "the old man walked home along the river tonight")

Per-layer mean look-back 3.68 / 7.87 / 8.69 / 10.03; model-wide 7.57; min look-back head L0H3 (3.48); max previous-character weight L0H3 (0.268); L0H2 is 3.81 / 0.242. Module's example card: L0H2, look-back 3.44, model-wide mean 6.5, prev-char weight 0.31 (labelled "representative, yours will differ"). Full 16-row table in `out/m03_02_headstats.txt`.

### 3.3 `m03_03_fast_attention.py` - 0.9-1.7 s

```
max abs diff: 0.0
equivalent
100 fwd: loop 0.162s  batched 0.207s  speedup 0.78x   (three runs: 0.78x, 0.78x, 0.81x; first run under load 1.07x)
```

| Module text | Real | Verdict |
|---|---|---|
| diff ~1e-6 or smaller, assert passes | 0.0, passes | match |
| "batched roughly 2-4x faster on CPU" | **0.78-0.81x (slower)** at (32, 64, 128), 2 threads | **wrong** here |

### 3.4 `m03_04_sinusoidal.py` - 197.9 s (contended; two 1,500-step trainings at BLOCK=32)

```
learned     best val 1.202 @ 1499   eval@32: 1.228   eval@48: IndexError: index out of range in self   eval@64: IndexError
sinusoidal  best val 1.358 @ 1499   eval@32: 1.383   eval@48: RuntimeError: The size of tensor a (32) must match the size of tensor b (48) at non-singleton dimension 2   eval@64: RuntimeError (64)
with the causal-mask buffer re-sized to L (ledger fix):  sinusoidal eval@48 1.866   eval@64 2.220
```

| Module text | Real | Verdict |
|---|---|---|
| learned 32: ~1.40; sinusoidal 32: ~1.42 | 1.228; 1.383 | differs (learned is better than sinusoidal, as expected for in-range) |
| learned 48 / 64: IndexError | IndexError | **match** |
| sinusoidal 48: ~1.55; 64: ~1.68 | **RuntimeError as written** (`Head.tril` is `block x block`); 1.866 / 2.220 after resizing the mask | module claim can't be produced with the module's own code |

### 3.5 `m03_05_ablate.py` - 1,500 steps each (mask-break 500); seconds are contended (9 in parallel)

| Config | Best val (step) | Final train / val | Seconds | Module (~) |
|---|---|---|---|---|
| baseline | **1.278** (750) | 0.411 / 1.336 | 199 | ~1.28 (match) |
| 1 head | 1.269 (700) | 0.466 / 1.302 | 161 | ~1.34, +0.06 |
| 1 layer | 1.271 (1450) | 0.869 / 1.294 | 58 | ~1.52, +0.24 |
| no MLP | 1.452 (1250) | 0.962 / 1.462 | 116 | ~1.58, +0.30 |
| no positional embedding | 1.632 (600) | 0.845 / 1.646 | 199 | ~1.85, +0.57 |
| no sqrt(d_k) scaling | **1.245** (600) | 0.278 / 1.352 | 199 | ~1.9-2.4 unstable, +0.6 |
| no residuals | 2.848 (850) | 2.843 / 2.849 | 196 | ~2.3, +1.0 |
| no mask (500 steps) | 0.066 (499); 0.166 at step 250 | 0.067 / 0.066 | 72 | "under 0.1, often under 0.05" (ok) |

No-mask generation: `'tttttttttttttttt...'` (repeated character), matching the module's "garbage, repeated characters". Deltas vs real baseline: 1 head -0.009, 1 layer -0.007, no MLP +0.174, no pos +0.354, no scaling -0.033, no residuals +1.570. Ordering of damage is therefore: no residuals (1.570) > no pos (0.354) > no MLP (0.174) > 1 head / 1 layer / no scaling (all within noise of baseline). The module's "biggest damage: residuals" is right; "no scaling unstable, +0.6" and "1 layer +0.24" are not reproduced. Mechanism prose about saturated softmax at d_k = 32 is not supported by this run (best val is lower than baseline, although final val 1.352 vs 1.336 shows slightly earlier overfitting).

---

## Module 4 (`module-04-how-llms-are-trained.md`)

Python blocks: 15 (incl. the indented round-trip test block in the mini-project). Runnable offline: 11. Scripts in `scripts/`, support files `scripts/m04_support/bpe.py` and `corpus.py` (verbatim copies of Part A and the Part B corpus).

### 4.1 Results (all identical to module text unless noted)

| Script | Seconds | Real output | Module | Verdict |
|---|---|---|---|---|
| `m04_01_bpe_demo` | 0.0 | 8 merges, `[257, 101, 260] [b'low', b'e', b'st']` | same | **match** |
| `m04_02_partB_corpus_bpe` | 0.1 | `characters: 1117 bytes: 1117 pretokens: 348`; merge 1 `he` count 34 ... merge 15 `rea` 9; merge 32 `team` 5; merge 33 `udent` 5; `token count: 760  bytes/token: 1.47`; `round-trip exact: True`; table 1117 / 720 (1.55) / 580 (1.93) / 504 (2.22) / 504 (2.22), merges 0 / 50 / 100 / 138 / 138 | same, including **138 merges, 760 tokens** | **match** |
| `m04_03_token_cost` | 0.0 | `$0.0320`, `$32.00`, `156` | same | match |
| `m04_04_sft_masking` | 0.7 | targets lists; `3.8008`, `4.0407` | same | match |
| `m04_05_reward_model` | 1.4 | BT loss 0.6931 / 0.0135 / 0.0017; weights +5.047 / +4.578 / -2.794 / -2.534 / -6.091; r1 +9.625, r6 +7.091, r2 +4.578, r3 -0.750, r4 -2.794, r5 -6.091; 10/10 | same | match |
| `m04_06_dpo_toy` | 1.6 | ref A=0.168 B=0.206 C=0.375 D=0.251; beta 0.2 trace (0.179 ... 0.997); sweep KL 1.213 / 1.760 / 1.709 / 1.557 / 0.566, loss 0.5317 / 0.2560 / 0.0513 / 0.0204 / 0.0020 | same | match |
| `m04_07_roundtrip_tests` (mini-project, tok = 456 vocab) | 0.1 | `all 10 round-trip tests passed` | claims all 10 pass | match |
| `m04_08_vocab_curve` (Practice 3) | 0.5 | 1117 / 855 (1.31) / 720 / 580 / 504 (2.22) x3; merges 0 / 20 / 50 / 100 / 138 / 138 / 138 | same | match |
| `m04_09_reward_break` (Practice 5) | 1.3 | `is_factually_correct +0.000`, other weights identical to Part D; r7 = r8 = +9.625 | same | match |
| `m04_10_dpo_contradiction` (Practice 6) | 1.3 | contradiction A=0.450 B=0.550 C=0.000 D=0.000 loss 0.3395; cycle A=0.168 B=0.206 C=0.375 D=0.251 loss 0.6931 | same | match |
| `m04_11_handcalc_bt` | 0.0 | P(a>b) 0.6682, P(d>a) 0.6225, P(a>c) 0.9168; c>d sigma **0.05215**, loss 2.954; a>c loss **0.0868**; BT loss at gap 2.0 = 0.1269; +100 shift unchanged 0.6682 | 0.05213 / 2.954 / 0.0869 / 0.127 | only 4th-decimal rounding differs |

Arithmetic in the Hindi/English answer: 36/183 = 0.197, 171/168 = 1.018 (ratio 5.17), $0.000072 vs $0.000342, $720 vs $3,420 per 10M messages all check out from the stated token counts (the token counts themselves were not reproduced; see skipped).

### 4.2 Skipped (needs the network / `transformers`)

- Part B "Compare against a production tokenizer" (block 5): gpt2 download; the `~250 tokens`, `~4.5 bytes/token` and the `Phot|osynthesis` split are **unverified**.
- Answer key 1 (block 10): gpt2 count on `my_essay.txt` (the 3,100-char essay is also not in the repo); 702 tokens, 4.42 b/tok, 2.7x, $0.0014 **unverified**.
- Answer key 4 (block 12): gpt2 English/Hindi token counts (36 and 171; 0.197 / 1.018 tok/char) **unverified**.
- Mini-project tokenizer-vs-GPT-2 table and JSON save/load cycle: not run (needs GPT-2 / user code).

---

## Files

- `scripts/`: `m01_*`, `m02_*`, `m03_*`, `m04_*` (+ `m04_support/`).
- `out/`: `<script>.txt` per run (stdout + stderr + `EXIT` / `WALL_SECONDS`); plots went to `out/run_m01_04/` (PNGs deleted after the run) and `tiny_gpt_m03.pt` there is required by `m03_02_headstats.py`.
- Re-run: `cd scripts && MPLBACKEND=Agg PYTHONPATH=.:m04_support python3 m0N_xxx.py` from a scratch directory (M3 head stats expects `tiny_gpt_m03.pt` in the cwd).

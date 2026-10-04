import time; _T=time.time()
from m02_lib import *
import statistics
rows = []
for cell in ["rnn", "gru", "lstm"]:
    finals, novs = [], []
    for seed in [0, 1, 2]:
        m, losses = train(cell, seed=seed)
        finals.append(losses[-1])
        s = sample(m, 60, temperature=1.0, seed=1)
        novs.append(sum(x not in TRAIN_SET for x in s))
    rows.append((cell, statistics.mean(finals),
                 max(finals) - min(finals), statistics.mean(novs)))
print("elapsed",round(time.time()-_T,1))
for r in rows:
    print(f"{r[0]:5s} loss {r[1]:.3f} (spread {r[2]:.3f})  novel {r[3]:.1f}/60")

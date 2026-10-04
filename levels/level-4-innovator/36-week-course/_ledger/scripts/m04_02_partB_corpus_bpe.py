import time; _T=time.time()
from bpe import BPETokenizer, pretokenize
from corpus import CORPUS

print("characters:", len(CORPUS),
      " bytes:", len(CORPUS.encode("utf-8")),
      " pretokens:", len(pretokenize(CORPUS)))

tok = BPETokenizer().train(CORPUS, vocab_size=256 + 40, verbose=True)
ids = tok.encode(CORPUS)
print("token count:", len(ids),
      "  bytes/token:", round(len(CORPUS.encode("utf-8")) / len(ids), 3))
print("round-trip exact:", tok.decode(ids) == CORPUS)

for vs in [256, 306, 356, 456, 656]:
    t = BPETokenizer().train(CORPUS, vocab_size=vs)
    n = len(t.encode(CORPUS))
    print(f"vocab {vs:5d}  merges {len(t.merges):4d}  tokens {n:5d}  "
          f"bytes/token {len(CORPUS.encode('utf-8')) / n:.2f}")
print("elapsed",round(time.time()-_T,2))

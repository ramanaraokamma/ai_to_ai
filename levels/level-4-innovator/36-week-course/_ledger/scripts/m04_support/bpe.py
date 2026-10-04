# LEDGER COPY of module-04 Part A block 1 (bpe.py), verbatim
"""A complete, correct byte-level BPE tokenizer in about 60 lines."""
import re
from collections import Counter

# Split text into runs of whitespace and runs of non-whitespace.
# Key property: "".join(pretokenize(text)) == text, for ANY text.
# Pre-tokenizing stops merges from ever crossing a word boundary.
PRETOKEN_RE = re.compile(r"\s+|\S+")


def pretokenize(text):
    return PRETOKEN_RE.findall(text)


def merge_pair(ids, pair, new_id):
    """Replace every adjacent occurrence of `pair` in `ids` with `new_id`."""
    out, i = [], 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(new_id)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out


class BPETokenizer:
    def __init__(self):
        self.merges = {}                                  # (id, id) -> new id
        self.vocab = {i: bytes([i]) for i in range(256)}   # id -> raw bytes

    def train(self, text, vocab_size, verbose=False):
        assert vocab_size >= 256, "vocab must include the 256 byte tokens"
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}

        # Work on UNIQUE chunks with counts — far faster than the raw stream.
        counts = Counter(pretokenize(text))
        words = [list(chunk.encode("utf-8")) for chunk in counts]
        freqs = list(counts.values())

        for m in range(vocab_size - 256):
            pair_counts = Counter()
            for word, f in zip(words, freqs):
                for p in zip(word, word[1:]):
                    pair_counts[p] += f
            if not pair_counts:
                break
            # Tie-break on smaller ids so training is fully deterministic.
            best, cnt = max(pair_counts.items(),
                            key=lambda kv: (kv[1], -kv[0][0], -kv[0][1]))
            if cnt < 2:
                break                                     # nothing left worth merging
            new_id = 256 + m
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            words = [merge_pair(w, best, new_id) for w in words]
            if verbose:
                print(f"merge {m + 1:3d}: {best} -> {new_id:4d}  "
                      f"{self.vocab[new_id]!r:14s} count={cnt}")
        return self

    def _encode_chunk(self, chunk):
        ids = list(chunk.encode("utf-8"))
        while len(ids) >= 2:
            pairs = set(zip(ids, ids[1:]))
            # Apply the EARLIEST-learned applicable merge, always.
            cand = min(pairs, key=lambda p: self.merges.get(p, float("inf")))
            if cand not in self.merges:
                break
            ids = merge_pair(ids, cand, self.merges[cand])
        return ids

    def encode(self, text):
        out = []
        for chunk in pretokenize(text):
            out.extend(self._encode_chunk(chunk))
        return out

    def decode(self, ids):
        return b"".join(self.vocab[i] for i in ids).decode("utf-8", errors="replace")

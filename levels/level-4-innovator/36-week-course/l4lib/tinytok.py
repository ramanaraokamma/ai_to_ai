"""tinytok.py - a from-scratch byte-level BPE tokenizer and a local token counter.

Used in week 20 (the student builds and tests the BPE) and weeks 23-36 (every place
that needs "how many tokens is this prompt?" for cost, context and truncation).

Nothing here downloads anything, and it never calls tiktoken.get_encoding (which
would fetch its ranks). No external tokenizer library is used. Stdlib only.

Pieces:
  BPETokenizer       train(text, vocab_size) / encode(text) / decode(ids) / save / load
  set_tokenizer(t)   install a trained tokenizer as the one count_tokens uses
  count_tokens(text) tokens from the installed BPE, else the fallback
                     len(text.split()) * 1.3  (rounded up, an estimate not a count)

Round trip: decode(encode(s)) == s for ANY string s, including emoji, Devanagari and "".
Training is deterministic: ties are broken on the smaller ids.
"""
import json
import math
import re
from collections import Counter

# Runs of whitespace and runs of non-whitespace. "".join(pretokenize(t)) == t for any t.
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
        self.merges = {}                                   # (id, id) -> new id, in learn order
        self.vocab = {i: bytes([i]) for i in range(256)}   # id -> raw bytes

    def train(self, text, vocab_size, verbose=False):
        """Learn up to vocab_size - 256 merges from `text`. Returns self."""
        assert vocab_size >= 256, "vocab must include the 256 byte tokens"
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}

        # Work on UNIQUE chunks with counts: far faster than the raw stream.
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
            best, cnt = max(pair_counts.items(),
                            key=lambda kv: (kv[1], -kv[0][0], -kv[0][1]))
            if cnt < 2:
                break                                      # nothing left worth merging
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
            cand = min(pairs, key=lambda p: self.merges.get(p, float("inf")))
            if cand not in self.merges:
                break
            ids = merge_pair(ids, cand, self.merges[cand])  # earliest-learned merge first
        return ids

    def encode(self, text):
        out = []
        for chunk in pretokenize(text):
            out.extend(self._encode_chunk(chunk))
        return out

    def decode(self, ids):
        return b"".join(self.vocab[i] for i in ids).decode("utf-8", errors="replace")

    @property
    def vocab_size(self):
        return len(self.vocab)

    def save(self, path):
        with open(path, "w") as f:
            json.dump([[a, b] for (a, b) in self.merges], f)

    @classmethod
    def load(cls, path):
        with open(path) as f:
            pairs = json.load(f)
        t = cls()
        for k, (a, b) in enumerate(pairs):
            t.merges[(a, b)] = 256 + k
            t.vocab[256 + k] = t.vocab[a] + t.vocab[b]
        return t


# ------------------------------------------------------------- token counter
_TOKENIZER = None


def set_tokenizer(tok):
    """Install a trained BPETokenizer for count_tokens (None removes it)."""
    global _TOKENIZER
    _TOKENIZER = tok


def get_tokenizer():
    return _TOKENIZER


def count_tokens(text):
    """Number of tokens in `text`.

    With a tokenizer installed: exactly len(encode(text)).
    Without: the estimate ceil(len(text.split()) * 1.3) (0 for empty text).
    """
    if _TOKENIZER is not None:
        return len(_TOKENIZER.encode(text))
    return math.ceil(len(text.split()) * 1.3 - 1e-9)

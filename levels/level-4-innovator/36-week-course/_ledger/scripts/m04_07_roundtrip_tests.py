from bpe import BPETokenizer
from corpus import CORPUS
tok = BPETokenizer().train(CORPUS, vocab_size=256 + 200)   # ledger: mini-project step 2 needs a `tok`
TESTS = [
    "",                                     # empty
    "a",                                    # single byte
    "The cricket team practised on Tuesday.",
    "Ramana works at Apple Inc.",
    "naïve café — résumé",                  # multi-byte UTF-8
    "नमस्ते दुनिया",                            # non-Latin script
    "🍕🍕 pizza time 🍕",                    # 4-byte emoji
    "def f(x):\n\treturn x**2  # tab + newline",
    "   \n\n   ",                           # whitespace only
    "aaaaaaaaaaaaaaaaaaaaaaaa",             # pathological repetition
]
for t in TESTS:
    assert tok.decode(tok.encode(t)) == t, repr(t)
print(f"all {len(TESTS)} round-trip tests passed")

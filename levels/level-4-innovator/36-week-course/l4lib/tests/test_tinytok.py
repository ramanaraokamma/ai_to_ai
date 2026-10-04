"""Plain-assert tests for l4lib/tinytok.py.  Run: python3 tests/test_tinytok.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import tinytok
from tinytok import BPETokenizer, count_tokens, set_tokenizer

TINY = "low low low low low lower lower widest widest widest"


def test_untrained_is_bytes():
    t = BPETokenizer()
    assert t.encode("abc") == [97, 98, 99]
    assert t.encode("") == []


def test_roundtrip_edge_cases():
    t = BPETokenizer().train(TINY * 3, vocab_size=256 + 10)
    for s in ["", " ", "\n\n", "hello world", "lowest", "\U0001F600 party \U0001F389",
              "नमस्ते दुनिया",
              "mixed é café 你好", "  leading and trailing  ", "a\tb\r\nc"]:
        assert t.decode(t.encode(s)) == s, repr(s)


def test_first_merges_are_known():
    t = BPETokenizer().train(TINY, vocab_size=256 + 3)
    # 'l','o' occurs in low*5 + lower*2 = 7 times; 'o','w' also 7; tie -> smaller first id
    assert list(t.merges.items())[0] == ((ord("l"), ord("o")), 256)
    assert t.vocab[256] == b"lo"


def test_merges_shorten_text():
    t = BPETokenizer().train(TINY, vocab_size=256 + 8)
    assert len(t.encode("lowest")) < len("lowest")
    assert len(t.encode(TINY)) < len(TINY.encode())


def test_deterministic():
    a = BPETokenizer().train(TINY, vocab_size=270)
    b = BPETokenizer().train(TINY, vocab_size=270)
    assert a.merges == b.merges and a.vocab == b.vocab


def test_stops_when_nothing_repeats():
    t = BPETokenizer().train("abcdefg", vocab_size=400)
    assert t.vocab_size == 256


def test_merges_do_not_cross_word_boundaries():
    t = BPETokenizer().train("ab ab ab ab ab ab", vocab_size=300)
    for b in t.vocab.values():
        assert b" " not in b or b.strip() == b""   # no token mixes space and letters


def test_save_load():
    t = BPETokenizer().train(TINY, vocab_size=270)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "m.json")
        t.save(p)
        u = BPETokenizer.load(p)
    assert u.merges == t.merges
    assert u.encode("lowest widest") == t.encode("lowest widest")


def test_count_tokens_fallback_and_installed():
    set_tokenizer(None)
    assert count_tokens("") == 0
    assert count_tokens("one two three four five") == 7      # ceil(5 * 1.3) = 7
    assert count_tokens("hello") == 2                         # ceil(1.3)
    t = BPETokenizer().train(TINY, vocab_size=270)
    set_tokenizer(t)
    try:
        assert count_tokens("lowest") == len(t.encode("lowest"))
    finally:
        set_tokenizer(None)


def test_no_external_tokenizer_imported():
    for name in ("tiktoken", "tokenizers", "transformers"):
        assert name not in tinytok.__dict__ and name not in sys.modules


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in tests:
        f()
    print(f"tinytok: all {len(tests)} tests passed")

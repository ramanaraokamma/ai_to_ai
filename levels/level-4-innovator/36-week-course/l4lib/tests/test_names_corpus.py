"""Plain-assert tests for l4lib/names.py and corpus.py.  Run: python3 tests/test_names_corpus.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import corpus
import names


def test_names_count_and_shape():
    assert len(names.NAMES) == 231 and len(set(names.NAMES)) == 231
    assert all(n.isalpha() and n.islower() and n.isascii() for n in names.NAMES)
    assert names.VOCAB_SIZE == 28 and names.MAXLEN == 8


def test_encode_decode_roundtrip():
    assert names.encode("aarav") == [2, 2, 19, 2, 23, 1, 0, 0]
    for n in names.NAMES:
        ids = names.encode(n)
        assert len(ids) == names.MAXLEN and names.decode(ids) == n


def test_corpus_size_and_charset():
    assert 6500 <= len(corpus.TEXT) <= 7500
    assert corpus.TEXT == corpus.TEXT.lower() and corpus.TEXT.isascii()
    assert corpus.TEXT.startswith("the sun rose") and not corpus.TEXT.endswith("\n")
    assert len(set(corpus.TEXT)) < 40


def test_toy_sentences_seeded():
    a = corpus.toy_sentences(50, seed=1)
    assert a == corpus.toy_sentences(50, seed=1)
    assert a != corpus.toy_sentences(50, seed=2)
    assert len(a) == 50
    for s in a:
        w = s.split()
        assert len(w) == 5 and w[0] == w[3] == "the"
        subj = " ".join(w[:2])
        obj = " ".join(w[-2:])
        assert subj != obj


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in tests:
        f()
    print(f"names/corpus: all {len(tests)} tests passed")

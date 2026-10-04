from bpe import *
if __name__ == "__main__":
    tiny = "low low low low low lower lower widest widest widest"
    t = BPETokenizer().train(tiny, vocab_size=256 + 8, verbose=True)
    ids = t.encode("lowest")
    print(ids, [t.vocab[i] for i in ids])

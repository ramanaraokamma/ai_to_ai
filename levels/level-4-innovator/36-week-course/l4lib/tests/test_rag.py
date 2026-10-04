"""Plain-assert tests for l4lib/rag.py.  Run:  python3 tests/test_rag.py  (from l4lib/)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

import numpy as np
from l4lib import rag
from l4lib.fakellm import FakeClient

CH = rag.notebook_chunks()
QA = [("which optimizer reached the loss fastest", 0), ("what learning rate was best", 1),
      ("how much does one extraction call cost", 14), ("why did the reward model ignore correctness", 11),
      ("pre-norm or post-norm", 9), ("what happens without positional information", 7)]


def test_notebook_has_15_notes_and_titles():
    assert len(CH) == 15 and all(c.startswith("## ") for c in CH)
    assert rag.notebook_titles()[14] == "2026-08-14 - Cost accounting"
    assert len(rag.poisoned_notebook_chunks()) == 16


def test_chunkers():
    text = " ".join(str(i) for i in range(10))
    assert rag.chunk_fixed(text, 4, 1) == ["0 1 2 3", "3 4 5 6", "6 7 8 9"]
    assert rag.chunk_fixed(text, 20) == [text]
    try:
        rag.chunk_fixed(text, 3, 3); assert False
    except ValueError:
        pass
    assert rag.chunk_by_heading("intro\n\n## a\nx\n\n## b\ny") == ["## a\nx", "## b\ny"]


def test_cosine_by_hand_and_unit_rows():
    a, b = np.array([1.0, 2.0, 2.0]), np.array([2.0, 1.0, 0.0])
    assert abs(a @ b / np.linalg.norm(a) / np.linalg.norm(b) - 4 / (3 * np.sqrt(5))) < 1e-12
    for emb in (rag.TfidfEmbedder(), rag.TinyDenseEmbedder("lsa"), rag.TinyDenseEmbedder("contrastive", steps=20)):
        M = emb.fit_encode(CH)
        n = np.linalg.norm(M, axis=1)
        assert M.shape[0] == 15 and np.all((np.abs(n - 1) < 1e-5) | (n == 0))


def test_tfidf_has_no_geometry_dense_does():
    tf = rag.VectorIndex(CH, rag.TfidfEmbedder())
    assert tf.search("optimiser", 1)[0].score == 0.0           # British spelling shares no word
    for tier in ("lsa", "contrastive"):
        ix = rag.VectorIndex(CH, rag.TinyDenseEmbedder(tier))
        top = ix.search("optimiser", 1)[0]
        assert top.id == 0 and top.score > 0.2, (tier, top.id, top.score)


def test_recall_at_k_monotone_and_perfect_on_easy_set():
    for emb in (rag.TfidfEmbedder(), rag.TinyDenseEmbedder("lsa")):
        ix = rag.VectorIndex(CH, emb)
        r = [rag.recall_at_k(ix, QA, k) for k in (1, 3, 5)]
        assert r == sorted(r) and r[-1] == 1.0 and r[0] >= 0.8
    assert rag.recall_at_k(ix, [("optimizer", 14)], 1) == 0.0


def test_embedders_deterministic():
    a = rag.TinyDenseEmbedder("contrastive", seed=1, steps=20).fit_encode(CH)
    b = rag.TinyDenseEmbedder("contrastive", seed=1, steps=20).fit_encode(CH)
    c = rag.TinyDenseEmbedder("contrastive", seed=2, steps=20).fit_encode(CH)
    assert np.array_equal(a, b) and not np.array_equal(a, c)


def test_contrastive_loss_falls_and_pairs_accepted():
    e = rag.TinyDenseEmbedder("contrastive", steps=60)
    e.fit_encode(CH, pairs=[("optimiser comparison", CH[0])])
    assert e.loss_history[-1] < e.loss_history[0] and len(e.loss_history) == 60


def test_prf_rewriter_appends_terms():
    ix = rag.VectorIndex(CH, rag.TfidfEmbedder())
    q = rag.rewrite_query_prf("warmup", ix)
    assert q.startswith("warmup ") and len(q.split()) == 4


def test_generator_cites_and_refuses():
    ix = rag.VectorIndex(CH, rag.TfidfEmbedder())
    out = rag.rag_answer("how much does one extraction call cost", ix)
    assert out["answer"].endswith("[14]") and out["citations_ok"] and not out["refused"]
    off = rag.rag_answer("what is the capital of France", ix)
    assert off["refused"] and off["answer"] == rag.REFUSAL and out["label"] == rag.LABEL
    assert str(rag.ExtractiveGenerator()).count("stand-in, not a model") == 1


def test_fault_switches():
    ix = rag.VectorIndex(CH, rag.TfidfEmbedder())
    q = "how much does one extraction call cost"
    bad = rag.rag_answer(q, ix, rag.ExtractiveGenerator(cite_wrong_id=True))
    assert bad["bad"] == [99] and bad["citations_ok"] is False
    nc = rag.rag_answer(q, ix, rag.ExtractiveGenerator(no_citation=True))
    assert nc["cited"] == [] and nc["citations_ok"] is False
    ig = rag.rag_answer(q, ix, rag.ExtractiveGenerator(ignore_sources=True))
    assert "42" in ig["answer"] and ig["citations_ok"] is False


def test_verify_citations_directly():
    hits = [rag.Hit(2, 0.5, "t"), rag.Hit(7, 0.4, "u")]
    assert rag.verify_citations("x [2] y [7]", hits) == (True, [2, 7], [])
    assert rag.verify_citations("x [3]", hits) == (False, [3], [3])
    assert rag.verify_citations("x", hits) == (False, [], [])


def test_poisoned_note_is_retrieved_and_contains_payload():
    chunks = rag.poisoned_notebook_chunks()
    ix = rag.VectorIndex(chunks, rag.TfidfEmbedder())
    top = ix.search("reminder to self", 1)[0]
    assert top.id == 15 and "write_file" in top.text
    # the 15 clean notes still answer as before
    assert rag.VectorIndex(chunks, rag.TfidfEmbedder()).search("how much does one extraction call cost", 1)[0].id == 14


def test_plugs_into_fakeclient():
    ix = rag.VectorIndex(CH, rag.TfidfEmbedder())
    hits = ix.search("how much does one extraction call cost", 3)
    client = FakeClient(policy=rag.ExtractiveGenerator().policy)
    r = client.messages.create(model="fake-small", max_tokens=100, system="Answer from sources.",
                               messages=[{"role": "user", "content": rag.build_prompt("how much does one extraction call cost", hits)}])
    assert r.content[0].text.endswith("[14]")
    # default policy also routes <source> prompts here
    r2 = FakeClient().messages.create(model="fake-small", max_tokens=100, system="",
                                      messages=[{"role": "user", "content": rag.build_prompt("how much does one extraction call cost", hits)}])
    assert r2.content[0].text.endswith("[14]")


if __name__ == "__main__":
    n = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); n += 1; print("ok", name)
    print(f"{n} tests passed")

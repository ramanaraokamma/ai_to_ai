"""A complete RAG core: chunking, embedding, and a vector index."""
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


# ------------------------------------------------------------------ chunking
def chunk_by_heading(text):
    """Split on markdown '## ' headings — the author's own boundaries."""
    parts = re.split(r"\n(?=## )", text)
    return [p.strip() for p in parts if p.strip().startswith("## ")]


def chunk_fixed(text, size, overlap):
    """Fixed word-count chunks with a sliding window."""
    words = text.split()
    step = max(1, size - overlap)
    out, i = [], 0
    while i < len(words):
        out.append(" ".join(words[i:i + size]))
        if i + size >= len(words):
            break
        i += step
    return out


# ----------------------------------------------------------------- embedders
def _unit(M):
    """L2-normalize each row so cosine similarity becomes a dot product."""
    n = np.linalg.norm(M, axis=1, keepdims=True)
    n[n == 0] = 1.0                       # never divide by zero
    return M / n


class TfidfEmbedder:
    """Sparse keyword baseline. Free, offline, and instructive when it fails."""
    name = "tfidf"

    def __init__(self):
        self.v = TfidfVectorizer(stop_words="english")

    def fit_encode(self, docs):
        return _unit(self.v.fit_transform(docs).toarray())

    def encode(self, texts):
        return _unit(self.v.transform(texts).toarray())


class MiniLMEmbedder:
    """Real dense embeddings. 384 dimensions. ~90 MB download on first use."""
    name = "minilm"

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.m = SentenceTransformer(model_name)

    def fit_encode(self, docs):
        return _unit(np.asarray(self.m.encode(docs)))

    def encode(self, texts):
        return _unit(np.asarray(self.m.encode(list(texts))))


# --------------------------------------------------------------------- index
class VectorIndex:
    def __init__(self, chunks, embedder):
        self.chunks = chunks
        self.emb = embedder
        self.M = embedder.fit_encode(chunks)     # N x d, unit rows

    def search(self, query, k=3):
        """Return [(chunk_id, similarity, text), ...] best first."""
        q = self.emb.encode([query])[0]
        sims = self.M @ q                         # cosine, because rows are unit
        order = np.argsort(-sims)[:k]
        return [(int(i), float(sims[i]), self.chunks[i]) for i in order]

    def __len__(self):
        return len(self.chunks)


import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from notes import NOTEBOOK
from rag import chunk_by_heading, VectorIndex, TfidfEmbedder
def build_index(): return VectorIndex(chunk_by_heading(NOTEBOOK), TfidfEmbedder())

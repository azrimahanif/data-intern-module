# tests/test_embeddings.py
import pytest
from submission.embeddings import OpenAIEmbeddings


@pytest.mark.skipif(not __import__('os').getenv("OPENAI_API_KEY"), reason="No API key")
def test_single_embedding():
    e = OpenAIEmbeddings()
    emb = e.create_embedding("Test embedding")
    assert emb is not None
    assert len(emb) == e.dimensions

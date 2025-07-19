import os
import pytest
from utils.rag_retriever import extract_text_from_pdf, get_embedding, retrieve_context

@pytest.mark.skipif(not os.path.exists("doc/TechEase_Customer_Support_Manual.pdf"), reason="PDF file not found")
def test_extract_text_from_pdf():
    chunks = extract_text_from_pdf("doc/TechEase_Customer_Support_Manual.pdf")
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert all(isinstance(c, str) for c in chunks)

def test_get_embedding():
    embedding = get_embedding("What is the return policy?")
    assert isinstance(embedding, list)
    assert len(embedding) > 10  # usually ~1000 dimensions

@pytest.mark.skipif(os.getenv("ULTRASAFE_API_KEY") is None, reason="API key not set")
def test_retrieve_context():
    results = retrieve_context("What is the return policy?", collection_name="support_collection")
    assert isinstance(results, list)

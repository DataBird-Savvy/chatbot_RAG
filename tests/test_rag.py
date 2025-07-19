import os
import pytest
from unittest.mock import patch, MagicMock
from utils.rag_retriever import SupportDocEmbedder


@pytest.fixture
def embedder():
    return SupportDocEmbedder(collection_name="test_collection")


def test_extract_text_from_pdf(embedder):
    # Create a small PDF for testing
    import fitz
    test_pdf = "test.pdf"
    doc = fitz.open()
    doc.insert_page(0, text="This is a test page.")
    doc.save(test_pdf)
    doc.close()

    result = embedder.extract_text_from_pdf(test_pdf)
    assert isinstance(result, list)
    assert "This is a test page." in result

    os.remove(test_pdf)


@patch("utils.rag_retriever.requests.post")
def test_get_embedding(mock_post, embedder):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": {
            "data": [{
                "embedding": [0.1, 0.2, 0.3]
            }]
        }
    }

    embedding = embedder.get_embedding("test query")
    assert isinstance(embedding, list)
    assert embedding == [0.1, 0.2, 0.3]


@patch.object(SupportDocEmbedder, "get_embedding")
@patch.object(SupportDocEmbedder, "extract_text_from_pdf")
def test_embed_and_store(mock_extract, mock_embed, embedder):
    mock_extract.return_value = ["Sample text"]
    mock_embed.return_value = [0.1, 0.2, 0.3]

    embedder.collection = MagicMock()
    embedder.embed_and_store("dummy.pdf")

    embedder.collection.add.assert_called_once()


@patch.object(SupportDocEmbedder, "get_embedding")
def test_retrieve_context(mock_embed, embedder):
    mock_embed.return_value = [0.1, 0.2, 0.3]
    embedder.collection = MagicMock()
    embedder.collection.query.return_value = {
        "documents": [["Answer 1", "Answer 2"]]
    }

    result = embedder.retrieve_context("test query")
    assert isinstance(result, list)
    assert "Answer 1" in result

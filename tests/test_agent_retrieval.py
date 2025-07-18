import pytest
from unittest.mock import patch, MagicMock
from agentapp.processing.agent_retrieval import retrieve_context


@patch("agentapp.processing.embedder.rerank")
@patch("agentapp.processing.embedder.get_embedding")
@patch("agentapp.processing.agent_retrieval.PersistentClient")
def test_retrieve_context_success(mock_client, mock_get_embedding, mock_rerank):
    
    mock_get_embedding.return_value = [0.1, 0.2, 0.3]
    mock_rerank.return_value = ["doc1", "doc2"]

    
    mock_collection = MagicMock()
    mock_collection.query.return_value = {"documents": [["doc2", "doc1"]]}
    mock_client.return_value.get_or_create_collection.return_value = mock_collection

    result = retrieve_context("AI in healthcare")

    assert result == ["doc1", "doc2"]
    mock_get_embedding.assert_called_once()
    mock_rerank.assert_called_once()



@patch("agentapp.processing.embedder.rerank")
@patch("agentapp.processing.embedder.get_embedding")
@patch("agentapp.processing.agent_retrieval.PersistentClient")
def test_retrieve_context_no_documents(mock_rerank, mock_get_embedding, mock_client):
    mock_get_embedding.return_value = [0.1, 0.2, 0.3]
    mock_rerank.return_value = []

    mock_collection = MagicMock()
    mock_collection.query.return_value = {"documents": [[]]}
    mock_client.return_value.get_or_create_collection.return_value = mock_collection

    result = retrieve_context("Non-relevant topic")
    assert result == []


@patch("agentapp.processing.agent_retrieval.get_embedding", side_effect=Exception("Mocked failure"))
def test_retrieve_context_exception(mock_get_embedding):
    result = retrieve_context("Will raise error")
    assert result == []  

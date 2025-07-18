import pytest
from unittest.mock import patch, MagicMock
from agentapp.processing import agent_retrieval


@patch.object(agent_retrieval.llm_toolkit, "get_embedding")
@patch.object(agent_retrieval.llm_toolkit, "rerank")
@patch.object(agent_retrieval.client, "get_or_create_collection")
def test_retrieve_context_success(mock_get_collection, mock_rerank, mock_get_embedding):
    mock_get_embedding.return_value = [0.1] * 768
    mock_collection = MagicMock()
    mock_collection.query.return_value = {"documents": [["doc1", "doc2", "doc3"]]}
    mock_get_collection.return_value = mock_collection
    mock_rerank.return_value = ["doc3", "doc1", "doc2"]

    result = agent_retrieval.retrieve_context("What is RAG in NLP?")
    assert result == ["doc3", "doc1", "doc2"]
    mock_get_embedding.assert_called_once()
    mock_rerank.assert_called_once()


@patch.object(agent_retrieval.llm_toolkit, "get_embedding")
@patch.object(agent_retrieval.client, "get_or_create_collection")
def test_retrieve_context_no_documents(mock_get_collection, mock_get_embedding):
    mock_get_embedding.return_value = [0.1] * 768
    mock_collection = MagicMock()
    mock_collection.query.return_value = {"documents": [[]]}  # no results
    mock_get_collection.return_value = mock_collection

    result = agent_retrieval.retrieve_context("Empty query test")
    assert result == []


@patch.object(agent_retrieval.llm_toolkit, "get_embedding", side_effect=Exception("Mock failure"))
def test_retrieve_context_exception(mock_get_embedding):
    result = agent_retrieval.retrieve_context("Should raise error")
    assert result == []

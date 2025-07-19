from agentapp.processing.embedder import LLMToolkit
from agentapp.processing.text_ops import chunk_text
from agentapp.logger import logging

llm = LLMToolkit()

def retrieve_context(query: str, top_k: int = 3) -> list[str]:
    """
    Fetch documents using LLM search and rerank based on semantic relevance.
    Returns a list of top-k document content strings.
    """
    logging.info(f"🔍 Retrieving documents for query: {query}")
    docs = llm.fetch_llm_research(query)

    if not docs:
        logging.warning("⚠️ No documents retrieved.")
        return []

    try:
        contents = [doc["content"] for doc in docs]
        reranked = llm.rerank(query, contents)

        # Return top-k reranked content strings
        top_reranked = reranked[:top_k]
        logging.info(f"✅ Retrieved and reranked {len(top_reranked)} documents.")
        return top_reranked

    except Exception as e:
        logging.error(f"❌ Reranking failed: {e}")
        return [doc["content"] for doc in docs[:top_k]]

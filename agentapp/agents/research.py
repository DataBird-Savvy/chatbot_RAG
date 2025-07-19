from agentapp.processing.embedder import LLMToolkit
from agentapp.logger import logging
from agentapp.exception import MultiAgentException
from utils.rag_retriever import SupportDocEmbedder


class ResearchAgent:
    def __init__(self):
        self.llm = LLMToolkit()
        self.retriever=SupportDocEmbedder()
        logging.info("ResearchAgent initialized.")

    def fetch_documents(self, query: str):
        logging.info(f"Fetching documents for query: '{query}'")

        try:
            
            llm_docs = self.llm.fetch_llm_research(query)
            logging.info(f"Fetched {len(llm_docs)} documents from LLM research.")
            llm_contents = [d["content"] for d in llm_docs]

            
            logging.info("Retrieving additional context from vector store.")
            retrieved_contents = self.retriever.retrieve_context(query)
            logging.info(f"Retrieved {len(retrieved_contents)} documents from vector store.")

            
            all_contents = llm_contents + retrieved_contents

            
            logging.info("Running reranker on combined content.")
            reranked_contents = self.llm.rerank(query, all_contents)
            logging.info("Reranking complete.")

            
            final_docs = []
            for content in reranked_contents:
                for d in llm_docs:
                    if d["content"] == content:
                        final_docs.append(d)
                        break
                else:
                    
                    final_docs.append({
                        "title": "Retrieved Context",
                        "content": content,
                        "url": ""
                    })

            logging.info(f"Returning {len(final_docs)} reranked documents.")
            return final_docs

        except Exception as e:
            logging.error(f"ResearchAgent: Failed to fetch documents: {e}")
            raise MultiAgentException(str(e))
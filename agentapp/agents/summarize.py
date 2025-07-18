# agentapp/agents/summarization_agent.py

from agentapp.processing.text_ops import chunk_text
from agentapp.processing.embedder import LLMToolkit
from agentapp.logger import logging
from agentapp.exception import MultiAgentException


class SummarizationAgent:
    def __init__(self, max_chunk_size=800):
        self.max_chunk_size = max_chunk_size
        self.llm = LLMToolkit()
        logging.info(f"SummarizationAgent initialized with max_chunk_size={self.max_chunk_size}")

    def summarize_document(self, text: str) -> str:
        logging.info("SummarizationAgent: Starting document summarization")

        try:
            logging.info("SummarizationAgent: Chunking input text")
            chunks = chunk_text(text, max_tokens=self.max_chunk_size)
            logging.info(f"SummarizationAgent: Total chunks created: {len(chunks)}")

            summarized_chunks = []

            for i, chunk in enumerate(chunks):
                logging.info(f"Summarizing chunk {i + 1}/{len(chunks)}")
                try:
                    summary = self.llm.get_summary(chunk)
                    summarized_chunks.append(summary)
                    logging.info(f"Successfully summarized chunk {i + 1}")
                except Exception as e:
                    logging.error(f"Failed to summarize chunk {i + 1}: {e}")
                    summarized_chunks.append("[Summary failed for this chunk]")

            if not summarized_chunks:
                raise MultiAgentException("No chunks could be summarized successfully.")

            final_summary = "\n".join(summarized_chunks)
            logging.info("SummarizationAgent: Finished summarizing all chunks")
            return final_summary

        except Exception as e:
            logging.error(f"SummarizationAgent: Document summarization failed: {e}")
            raise MultiAgentException(f"SummarizationAgent failed: {e}")

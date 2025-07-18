# agentapp/agents/critic.py

from agentapp.logger import logging
from agentapp.processing.embedder import LLMToolkit  
from agentapp.exception import MultiAgentException


class CriticAgent:
    def __init__(self):
        self.llm = LLMToolkit()
        logging.info("CriticAgent initialized.")

    def evaluate_summary(self, summary: str) -> dict:
        logging.info("CriticAgent: Evaluating summary quality.")

        try:
            logging.info(f"CriticAgent: Summary content to evaluate (truncated):\n{summary[:200]}...")
            label = self.llm.get_critique_score(summary)
            logging.info(f"CriticAgent: Evaluation completed with label: {label}")

            return {"summary": summary, "label": label}

        except Exception as e:
            logging.error(f"CriticAgent: Failed to evaluate summary: {e}")
            raise MultiAgentException(f"CriticAgent failed to evaluate summary: {e}")

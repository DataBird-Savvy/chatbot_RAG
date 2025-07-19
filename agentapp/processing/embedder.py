import requests
import os
import time
from dotenv import load_dotenv
from agentapp.logger import logging

load_dotenv()

ULTRASAFE_API_KEY = os.getenv("ULTRASAFE_API_KEY")
HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": ULTRASAFE_API_KEY
}


class LLMToolkit:
    def __init__(self):
        self.base_url = "https://api.us.inc/usf/v1/hiring"
        logging.info("LLMToolkit initialized with base URL: %s", self.base_url)

    def fetch_llm_research(self, query: str, limit: int = 3) -> list:
        logging.info(f"LLMToolkit: fetching research for query: '{query}' with limit={limit}")
        
        prompt = f"""List {limit} recent academic findings or insights on the topic: "{query}".
        Format each result as:
        - Title: ...
        - Key insight: ...
        - (Optional) Source: ...
        """

        payload = {
            "model": "usf1-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "stream": False,
            "max_tokens": 1000
        }

        try:
            start = time.time()
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=HEADERS)
            response.raise_for_status()
            elapsed = time.time() - start
            logging.info(f"LLMToolkit: research fetched successfully in {elapsed:.2f} seconds")

            content = response.json()["choices"][0]["message"]["content"]

            # Parsing response
            docs = []
            current_doc = {}
            for line in content.strip().split("\n"):
                line = line.strip()
                if line.startswith("- Title:"):
                    if current_doc:
                        docs.append(current_doc)
                    current_doc = {"title": line[8:].strip(), "content": "", "url": ""}
                elif line.startswith("- Key insight:"):
                    current_doc["content"] = line[14:].strip()
                elif line.startswith("- Source:"):
                    current_doc["url"] = line[9:].strip()
            if current_doc:
                docs.append(current_doc)

            logging.info(f"LLMToolkit: total {len(docs)} documents structured and returned")
            return docs

        except Exception as e:
            logging.error(f"LLMToolkit: LLM research failed: {e}")
            return []

    def get_summary(self, text: str) -> str:
        logging.info(f"LLMToolkit: summarizing text of length {len(text)}")
        
        payload = {
            "model": "usf1-mini",
            "messages": [
                {"role": "system", "content": "Summarize this academic text."},
                {"role": "user", "content": text}
            ],
            "temperature": 0.7,
            "stream": False,
            "max_tokens": 1000
        }

        try:
            start = time.time()
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=HEADERS)
            response.raise_for_status()
            elapsed = time.time() - start
            logging.info(f"LLMToolkit: summarization completed in {elapsed:.2f} seconds")

            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"LLMToolkit: Summarization failed: {e}")
            return "Summarization failed."

 
    def rerank(self, query: str, texts: list[str]) -> list[str]:
        logging.info(f"LLMToolkit: reranking {len(texts)} documents against query: '{query}'")

        payload = {
            "model": "usf1-rerank",
            "query": query,
            "texts": texts
        }

        try:
            response = requests.post(f"{self.base_url}/embed/reranker", json=payload, headers=HEADERS)
            response.raise_for_status()
            results = response.json()["result"]["data"]
            ranked = sorted(results, key=lambda x: x["score"], reverse=True)

            logging.info("LLMToolkit: reranking completed successfully")
            return [item["text"] for item in ranked]
        except Exception as e:
            logging.error(f"LLMToolkit: Reranking failed: {e}")
            return texts

    def get_critique_score(self, summary: str) -> str:
        logging.info("LLMToolkit: evaluating critique score for summary")
        logging.info(f"LLMToolkit: Summary preview: {summary[:100]}...")

        prompt = f"""You are a summary critic.
Evaluate the following summary for quality in terms of clarity, depth, and relevance.
Respond with one word: High, Medium, or Low.

Summary:
\"\"\"{summary}\"\"\"
"""
        payload = {
            "model": "usf1-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "stream": False,
            "max_tokens": 1000
        }

        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=HEADERS)
            response.raise_for_status()
            message = response.json()["choices"][0]["message"]["content"]

            label = message.strip().split()[0].lower()
            if label in ["high", "medium", "low"]:
                logging.info(f"LLMToolkit: critique score = {label.capitalize()}")
                return label.capitalize()
            logging.warning("LLMToolkit: Unexpected critique score response")
            return "Unknown"
        except Exception as e:
            logging.error(f"LLMToolkit: Critique scoring failed: {e}")
            return "Unknown"
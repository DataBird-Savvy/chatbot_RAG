import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv
import os
from chromadb import PersistentClient
from app.logger import logging

logger = logging.getLogger(__name__)

load_dotenv()

# ---------- Initialize Persistent ChromaDB client ----------
client = PersistentClient(path="chroma_store")  # Persistent DB store

# ---------- Extract text from PDF ----------
def extract_text_from_pdf(path: str) -> list[str]:
    try:
        logger.info(f"Extracting text from: {path}")
        doc = fitz.open(path)
        texts = [page.get_text() for page in doc]
        doc.close()
        return [t.strip() for t in texts if t.strip()]
    except Exception as e:
        logger.error(f"Error reading PDF [{path}]: {e}")
        raise

# ---------- Call USF API to get embeddings ----------
def get_embedding(text: str):
    try:
        url = "https://api.us.inc/usf/v1/embed/embeddings"
        payload = {
            "model": "usf1-embed",
            "input": text
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("ULTRASAFE_API_KEY")
        }
        logger.info("Calling embedding API")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        embedding = response.json()["result"]["data"][0]["embedding"]

        if embedding is None:
            logger.error(f"Embedding not found in response: {response.json()}")
            raise ValueError("Missing 'embedding' in API response")

        return embedding

    except Exception as e:
        logger.error(f"Embedding API call failed: {e}")
        raise

# ---------- Store embedded chunks ----------
def embed_and_store(pdf_path: str, collection_name: str = "support_collection"):
    logger.info(f"Embedding and storing chunks from {pdf_path} into collection: {collection_name}")
    try:
        chunks = extract_text_from_pdf(pdf_path)
        collection = client.get_or_create_collection(name=collection_name)

        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            chunk_id = f"{os.path.basename(pdf_path)}_chunk_{i}"
            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[chunk_id]
            )
            logger.info(f"Stored chunk ID: {chunk_id} in {collection_name}")
        

    except Exception as e:
        logger.error(f"Failed to embed and store chunks from {pdf_path} in {collection_name}: {e}")
        raise

# ---------- Rerank results ----------
def rerank_results(query: str, texts: list[str]) -> list[str]:
    try:
        url = "https://api.us.inc/usf/v1/embed/reranker"
        payload = {
            "model": "usf1-rerank",
            "query": query,
            "texts": texts
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("ULTRASAFE_API_KEY")
        }
        logger.info("Calling rerank API")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"Reranked Response received: {response.json()}")
        data = response.json()["result"]["data"]
        reranked = sorted(data, key=lambda x: x["score"], reverse=True)
        return [item["text"] for item in reranked]

    except Exception as e:
        logger.error(f"Rerank API call failed: {e}")
        return texts  # fallback

# ---------- Retrieve context ----------
def retrieve_context(query: str, collection_name: str = "support_collection", top_k: int = 2):
    try:
        logger.info(f"Retrieving context from '{collection_name}' for query: {query}")
        collection = client.get_or_create_collection(name=collection_name)
        logger.info(f"collection count: {collection.count()}")

        query_embedding = get_embedding(query)
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        documents = results.get('documents', [[]])[0] if results.get('documents') else []
        logger.info(f"Retrieved {len(documents)} documents from ChromaDB")

        if documents:
            reranked_docs = rerank_results(query, documents)
            logger.info(f"Reranked documents: {reranked_docs}")
            return reranked_docs

        return []

    except Exception as e:
        logger.error(f"Context retrieval failed from '{collection_name}': {e}")
        return []

# ---------- Run as script ----------
if __name__ == "__main__":
    embed_and_store("doc/TechEase_Customer_Support_Manual.pdf", collection_name="support_collection")
    result = retrieve_context("What is the return policy?", collection_name="support_collection")
    print(result)

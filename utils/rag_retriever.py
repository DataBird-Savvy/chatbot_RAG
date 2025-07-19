import fitz  
import requests
from dotenv import load_dotenv
import os
from chromadb import PersistentClient

load_dotenv()


class SupportDocEmbedder:
    def __init__(self, db_path: str = "chroma_store", collection_name: str = "default"):
        self.client = PersistentClient(path=db_path)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        self.api_key = os.getenv("ULTRASAFE_API_KEY")

    def extract_text_from_pdf(self, path: str) -> list[str]:
        try:
            
            doc = fitz.open(path)
            texts = [page.get_text().strip() for page in doc if page.get_text().strip()]
            doc.close()
            return texts
        except Exception as e:
            
            raise

    def get_embedding(self, text: str):
        try:
            url = "https://api.us.inc/usf/v1/embed/embeddings"
            payload = {
                "model": "usf1-embed",
                "input": text
            }
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            embedding = response.json()["result"]["data"][0]["embedding"]

            if embedding is None:
                
                raise ValueError("Missing 'embedding' in API response")

            return embedding

        except Exception as e:
            
            raise

    def embed_and_store(self, pdf_path: str):
        
        try:
            chunks = self.extract_text_from_pdf(pdf_path)

            for i, chunk in enumerate(chunks):
                embedding = self.get_embedding(chunk)
                chunk_id = f"{os.path.basename(pdf_path)}_chunk_{i}"
                self.collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    ids=[chunk_id]
                )
                
        except Exception as e:
            
            raise


    def retrieve_context(self, query: str, top_k: int = 2):
        try:
            
            query_embedding = self.get_embedding(query)
            results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
            documents = results.get('documents', [[]])[0] if results.get('documents') else []
          

            return documents

        except Exception as e:
            
            return []


# ---------- Run as script ----------
if __name__ == "__main__":
    # support_agent = SupportDocEmbedder(collection_name="support_collection")
    # support_agent.embed_and_store("doc/TechEase_Customer_Support_Manual.pdf")
    # result = support_agent.retrieve_context("What is the return policy?")
    # print(result)
    support_agent = SupportDocEmbedder(collection_name="research_collection")
    support_agent.embed_and_store("doc/healthAI.pdf")
    result = support_agent.retrieve_context("AI in healthcare")
    print(result)

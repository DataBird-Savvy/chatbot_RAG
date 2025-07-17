from app.core.rag_pipeline import embed_and_store
import os

pdf_dir = "doc"
for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith(".pdf"):
        embed_and_store(os.path.join(pdf_dir, pdf_file))

print("All PDFs embedded and stored.")

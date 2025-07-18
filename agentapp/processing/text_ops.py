# agentapp/processing/text_ops.py

from agentapp.logger import logging

def chunk_text(text: str, max_tokens: int = 800) -> list[str]:
    logging.info(f"chunk_text: Starting to chunk text with max_tokens={max_tokens}")
    
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_tokens:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    logging.info(f"chunk_text: Total chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3]):
        logging.info(f"chunk_text: Preview chunk {i+1}: {chunk[:100]}...")

    return chunks

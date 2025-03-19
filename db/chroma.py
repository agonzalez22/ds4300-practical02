import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="notes")

embed_fn = embedding_functions.DefaultEmbeddingFunction()

def add_text(pdf_title: str, text: str, overlap_size: int, model: str, start: int, end: int):
    collection.add(
        documents=[text],
        metadatas={
            "model": model,
            "chunk_size": len(text),
            "overlap_size": overlap_size,
            "pdf_title": pdf_title,
            "start_page": start,
            "end_page": end
        },
        embeddings=embed_fn(text))
import numpy as np
import chromadb
from chromadb.utils import embedding_functions

def add_text_to_chroma(pdf_title: str, text: str, overlap_size: int, embedding: np.array, model: str):
    chroma_client = chromadb.PersistentClient()
    collection = chroma_client.get_or_create_collection(name="notes")

    collection.upsert(
        documents=text,
        metadatas={
            "model": model,
            "chunk_size": len(text),
            "overlap_size": overlap_size,
        },
        embeddings=embedding,
        ids=pdf_title
    )

def query_chroma(embedding: list) -> dict:
    chroma_client = chromadb.PersistentClient()
    collection = chroma_client.get_or_create_collection(name="notes")

    results = collection.query(query_embeddings=embedding, n_results=1)
    return results
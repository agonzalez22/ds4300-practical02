import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="notes")

embed_fn = embedding_functions.DefaultEmbeddingFunction()


def add_text_to_chroma(pdf_title: str, text: str, overlap_size: int, model: str):
    collection.add(
        documents=[text],
        metadatas={
            "model": model,
            "chunk_size": len(text),
            "overlap_size": overlap_size,
            "pdf_title": pdf_title,
        },
        embeddings=embed_fn([text]),
        ids=[],  # idk bro
    )


def query_chroma(embedding: list) -> dict:
    results = collection.query(query_embeddings=embedding, n_results=5)

    return results

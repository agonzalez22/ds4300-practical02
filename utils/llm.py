import numpy as np
import ollama
from sentence_transformers import SentenceTransformer


def get_embedding(
    text: str, model: str = "nomic-embed-text", sentence_transformer=True
) -> list:
    """Generate an embedding using nomic-embed-text"""
    if sentence_transformer:
        model = SentenceTransformer(model)
        embeddings = np.array(model.encode(text))
        return embeddings
    else:
        response = ollama.embeddings(model=model, prompt=text)
        return np.array(response["embedding"])

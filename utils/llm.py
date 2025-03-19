import numpy as np
import ollama
from sentence_transformers import SentenceTransformer


def get_embedding(
    text: str, model: str
) -> list:
    """Generate an embedding using nomic-embed-text"""
    try:
        response = ollama.embeddings(model=model, prompt=text)
        return np.array(response["embedding"])
    except: # figure out which error to handle here (or leave it)
        model = SentenceTransformer(model)
        embeddings = np.array(model.encode(text))
        return embeddings

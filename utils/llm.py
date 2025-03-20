import numpy as np
import ollama
from sentence_transformers import SentenceTransformer


def get_embedding(text: str, model: str) -> list:
    """Generate an embedding using nomic-embed-text"""
    try:
        response = ollama.embeddings(model=model, prompt=text)
        return np.array(response["embedding"])
    except:  # figure out which error to handle here (or leave it)
        model = SentenceTransformer(model)
        embeddings = np.array(model.encode(text))
        return embeddings


def get_llm_response(query: str, response: str, model="mistral"):
    print("Generating LLM response...")

    prompt = f"Given the query: {query}, and the response: {response}, summarize the information."

    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

    print("Response Generated!")
    return response

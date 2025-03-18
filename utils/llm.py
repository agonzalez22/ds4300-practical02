import ollama

def get_embedding(text: str, model: str = "nomic-embed-text") -> list:
    """ Generate an embedding using nomic-embed-text"""
    response = ollama.embeddings(model=model, prompt=text)
    return response["embedding"]
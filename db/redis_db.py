import ollama
import redis
import numpy as np
from redis.commands.search.query import Query
from llm import get_embedding


# Initialize Redis connection
redis_client = redis.Redis(host="localhost", port=6379, db=0)

VECTOR_DIM = 768
INDEX_NAME = "embedding_index"
DOC_PREFIX = "doc:"
DISTANCE_METRIC = "COSINE"


# Create an index in Redis
def create_hnsw_index():
    try:
        redis_client.execute_command(f"FT.DROPINDEX {INDEX_NAME} DD")
    except redis.exceptions.ResponseError:
        pass

    redis_client.execute_command(
        f"""
        FT.CREATE {INDEX_NAME} ON HASH PREFIX 1 {DOC_PREFIX}
        SCHEMA text TEXT
        embedding VECTOR HNSW 6 DIM {VECTOR_DIM} TYPE FLOAT32 DISTANCE_METRIC {DISTANCE_METRIC}
        """
    )
    print("Index created successfully.")



def store_embedding(doc_id: str, text: str, embedding: list, model: str, chunksize: int, overlap: int, PDF: str, start:int, end:int):
    key = f"{DOC_PREFIX}{doc_id}"
    redis_client.hset(
        key,
        mapping={
            "text": text,
            "embedding": np.array(
                embedding, dtype=np.float32
            ).tobytes(), 
            "model": model,
            "chunksize": chunksize,
            "overlap": overlap,
            "PDF": PDF, 
            "start": start,
            "end": end
        },
    )
    # print(f"Stored embedding for: {text}")

    # texts = [
    #     "Redis is an in-memory key-value database.",
    #     "Ollama provides efficient LLM inference on local machines.",
    #     "Vector databases store high-dimensional embeddings for similarity search.",
    #     "HNSW indexing enables fast vector search in Redis.",
    #     "Ollama can generate embeddings for RAG applications.",
    # ]



    # for i, text in enumerate(texts):
    #     embedding = get_embedding(text)
    #     store_embedding(str(i), text, embedding)

    # query_text = "Efficient search in vector databases"

    # q = (
    #     Query("*=>[KNN 3 @embedding $vec AS vector_distance]")
    #     .sort_by("vector_distance")
    #     .return_fields("id", "vector_distance")
    #     .dialect(2)
    # )
    # query_text = "Efficient search in vector databases"
    # embedding = get_embedding(query_text)
    # res = redis_client.ft(INDEX_NAME).search(
    #     q, query_params={"vec": np.array(embedding, dtype=np.float32).tobytes()}
    # )
    # print(res.docs)

store_embedding()
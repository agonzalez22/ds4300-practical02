import os
import psutil
import time
import csv
from utils.llm import *
from utils.ingest import *
from db.chroma import *
from db.postgres import *
from db.redis_db import *

CHUNK_SIZES = [200, 500, 1000]
OVERLAP_SIZES = [0, 50, 100]
EMBEDDING_MODELS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
    "InstructorXL"
]
VECTOR_DB_OPTIONS = ["chroma", "redis", "postgres"]
LLM_MODELS = ["gemma2:2b", "mistral"]
QUERIES = ["When are linked lists faster than contiguously-allocated lists?",
           "Why is a B+ Tree a better than an AVL tree when indexing a large dataset?",
           "What is disk-based indexing and why is it important for database systems?"]

def run_pipeline(chunk_size, overlap_size, embedding_model, vector_db, query, llm_model):   
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss
    start_time = time.time()

    e = get_embedding(query, embedding_model)

    if vector_db == 'redis':
        res = query_redis(e)
        res = get_llm_response(query, res[0]["text"], llm_model)
    elif vector_db == 'chroma':
        res = query_chroma(e)
        res = get_llm_response(query, res, llm_model)
    elif vector_db == 'postgres':
        res = query_postgres(e)
        res = get_llm_response(query, res[0]["text"], llm_model)

    result = {
        "chunk_size": chunk_size,
        "overlap_size": overlap_size,
        "embedding_model": embedding_model,
        "vector_db": vector_db,
        "query": query,
        "llm_model": llm_model,
        "response": res.message.content
    }
    
    end_time = time.time()
    memory_after = process.memory_info().rss 
    elapsed_time = end_time - start_time
    memory_usage = (memory_after - memory_before) / 1024 / 1024  # in mb

    print(f"Time: {elapsed_time:.2f} seconds")
    print(f"Memory Usage: {memory_usage:.2f} MB")

    return result


def main():
    results = []
    for chunk_size in CHUNK_SIZES:
        for overlap_size in OVERLAP_SIZES:
            for embedding_model in EMBEDDING_MODELS:
                for vector_db in VECTOR_DB_OPTIONS:
                    for query in QUERIES:
                        for llm_model in LLM_MODELS:
                            folder = os.getenv("PDF_PATH")
                            print("Starting...")
                            
                            for f in os.listdir(folder):
                                curr_pdf = PDF(f"{folder}{f}")
                                curr_pdf.process(chunk_size=chunk_size, overlap_size=overlap_size, model=llm_model)
                                
                            if vector_db == 'redis':
                                curr_pdf.ingest(store_embedding)
                            elif vector_db == 'chroma':
                                curr_pdf.ingest(add_text_to_chroma) 
                            elif vector_db == 'postgres':
                                curr_pdf.ingest(add_text_to_postgres_db) 

                            print(curr_pdf.title)
            
                            result = run_pipeline(chunk_size, overlap_size, embedding_model, vector_db, query, llm_model)
                            results.append(result)
    
    headers = ["chunk_size", "overlap_size", "embedding_model", "vector_db", "query", "llm_model", "response"]
    with open("test.csv", mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(results)

def __init__():
    main()
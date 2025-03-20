import os
import sys

import numpy as np
import psycopg2
from dotenv import load_dotenv
from supabase import create_client, Client
import vecs

load_dotenv()

URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
DB_NAME=os.environ.get("SUPABASE_NAME")
DB_CONNECTION = os.environ.get("SUPABASE_CONNECTION")

supabase = create_client(URL, KEY)


def add_text_to_postgres_db(pdf_title:str, text: str, overlap_size: int,  embedding: np.array, model: str):
    """ 
    """
#     new = {"text": text, 
#            "embedding": list(embedding), 
#            "model": model, 
#            "chunk_size": len(text), 
#            "overlap_size": overlap_size, 
#            "pdf_title": pdf_title}

#     response = (
#     supabase.table(DB_NAME)
#     .insert(new)
#     .execute()
# )
    vx = vecs.create_client(DB_CONNECTION)
    docs = vx.get_or_create_collection(name="vector_db", dimension=768)
    # add records to the collection
    docs.upsert(
        [
            (
            pdf_title,  # ????
            list(embedding),  # maybe... change this to lst
            {"text": text,  
           "model": model, 
           "chunk_size": len(text), 
           "overlap_size": overlap_size, 
           "pdf_title": pdf_title} # freak 
            )
        ]
    )
    vx.disconnect()
    print("yipee! did it.")


def query_postgres(embedding: list) -> dict: 
    """ gets embeddings"""
    vx = vecs.create_client(DB_CONNECTION)
    docs = vx.get_or_create_collection(name="vector_db", dimension=768)

    res = docs.query(
        list(embedding),   # required
        limit=1,                         # (optional) number of 
        measure=vecs.IndexMeasure.cosine_distance,       
        include_metadata=True,          # (optional) should record metadata be returned?
    )

    vx.disconnect()

    print("Successfully queried!")

    return res


# def connect():
#     """connect to the db, returns connection obj

#     * if connection is closed: 0, that means connection is OPEN
#     """
#     conn = psycopg2.connect(
#         database="postgres",  # leave hardcoded?
#         host="localhost",
#         user="postgres",
#         password=os.getenv("POSTGRES_PASS"),
#         port="5432",
#     )
#     return conn


# def add_text_to_postgres_db(pdf_title:str, text: str, overlap_size: int,  embedding: np.array, model: str, start: int, end: int):
#     """transaction to create new instance in table

#         id SERIAL primary key, 
#         text TEXT, 
#         embedding vector(768), 
#         model TEXT, 
#         chunk_size INT, 
#         overlap_size INT, 
#         pdf_title TEXT, 
#         start_page INT, 
#         end_page INT, 
#     """
#     conn = connect()
#     cur = conn.cursor()

#     cur.execute(
#         """
#     INSERT INTO notes (text, embedding, model, chunk_size, overlap_size, pdf_title, start_page, end_page)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
# """,
#         (text, embedding, model, len(text), overlap_size, pdf_title, start, end),
#     )

#     conn.commit()

#     cur.close()
#     conn.close()  # make sure this closes because transactions are evil lowk

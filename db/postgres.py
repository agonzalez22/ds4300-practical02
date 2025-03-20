import os
import sys

import numpy as np
import psycopg2
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
DB_NAME=os.environ.get("SUPABASE_NAME")
supabase = create_client(URL, KEY)

def add_text_to_postgres_db(pdf_title:str, text: str, overlap_size: int,  embedding: np.array, model: str):
    """ 
    """
    new = {"text": text, 
           "embedding": list(embedding), 
           "model": model, 
           "chunk_size": len(text), 
           "overlap_size": overlap_size, 
           "pdf_title": pdf_title}

    response = (
    supabase.table(DB_NAME)
    .insert(new)
    .execute()
)

def get_embeddings(query: str) -> dict: 
    """ gets embeddings"""
    response = (supabase.table(DB_NAME)
        .select(query) # ...
        .execute()
    )


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

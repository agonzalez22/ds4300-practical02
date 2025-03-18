import os
import sys

import numpy as np
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect():
    """connect to the db, returns connection obj

    * if connection is closed: 0, that means connection is OPEN
    """
    conn = psycopg2.connect(
        database="postgres",  # leave hardcoded?
        host="localhost",
        user="postgres",
        password=os.getenv("POSTGRES_PASS"),
        port="5432",
    )
    return conn


def add_text_to_postgres_db(pdf_title:str, text: str, overlap_size: int,  embedding: np.array, model: str, start: int, end: int):
    """transaction to create new instance in table
    
        id SERIAL primary key, 
        text TEXT, 
        embedding vector(768), 
        model TEXT, 
        chunk_size INT, 
        overlap_size INT, 
        pdf_title TEXT, 
        start_page INT, 
        end_page INT, 
    """
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
    INSERT INTO notes (text, embedding, model, chunk_size, overlap_size, pdf_title, start_page, end_page)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""",
        (text, embedding, model, len(text), overlap_size, pdf_title, start, end),
    )

    conn.commit()

    cur.close()
    conn.close()  # make sure this closes because transactions are evil lowk

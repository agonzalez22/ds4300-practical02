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


def add_text_to_postgres_db(text: str, embedding: np.array, model: str):
    """transaction to create new instance in table"""
    # find the embedding length, and size
    embed_size = len(embedding)
    size_kb = sys.getsizeof(embedding.tobytes()) / 1024
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
    INSERT INTO notes (text, embedding, model, embedding_size, size_kb)
    VALUES (%s, %s, %s, %s, %s)
""",
        (text, embedding, model, embed_size, size_kb),
    )

    conn.commit()

    cur.close()
    conn.close()  # make sure this closes because transactions are evil lowk

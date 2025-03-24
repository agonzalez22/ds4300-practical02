import os
import sys

import numpy as np
# import psycopg2
import vecs
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
DB_NAME = os.environ.get("SUPABASE_NAME")
DB_CONNECTION = os.environ.get("SUPABASE_CONNECTION")

supabase = create_client(URL, KEY)


def add_text_to_postgres_db(
    pdf_title: str, text: str, overlap_size: int, embedding: np.array, model: str
):
    """ """
    vx = vecs.create_client(DB_CONNECTION)
    docs = vx.get_or_create_collection(name="vector_db", dimension=768)
    # add records to the collection
    docs.upsert(
        [
            (
                pdf_title,  # ????
                list(embedding),  # maybe... change this to lst
                {
                    "text": text,
                    "model": model,
                    "chunk_size": len(text),
                    "overlap_size": overlap_size,
                    "pdf_title": pdf_title,
                },  # freak
            )
        ]
    )
    vx.disconnect()
    print("yipee! did it.")


def query_postgres(embedding: list) -> dict:
    """gets embeddings"""
    vx = vecs.create_client(DB_CONNECTION)
    docs = vx.get_or_create_collection(name="vector_db", dimension=768)

    res = docs.query(
        list(embedding),  # required
        limit=1,  # (optional) number of
        measure=vecs.IndexMeasure.cosine_distance,
        include_metadata=True,  # (optional) should record metadata be returned?
    )

    vx.disconnect()

    print("Successfully queried!")

    return res

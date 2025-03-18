import os

import fitz  # pdf reader thing
from dotenv import load_dotenv

from .llm import get_embedding

load_dotenv()


def ingest_pdf():
    """ingests the pdf text"""
    pdf_path = os.getenv("PDF_PATH")

    text = ""
    for f in os.listdir(pdf_path):
        doc = fitz.open(
            f"{pdf_path}{f}"
        )  # TODO: we want to update db row to be per doc ? or per page idk
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text")

    return text


def process_pdf(text):
    """process text"""
    #embedding = get_embedding(text, 'all-MiniLM-L6-v2')  # vectorize
    embedding = get_embedding(text, sentence_transformer=False)
    # TODO: generate 5 different embeddings per each document, just store them as attr in the db
    return embedding # testing


def remove_stop(text):
    pass


print(process_pdf(ingest_pdf()))

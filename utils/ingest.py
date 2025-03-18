import os

import fitz  # pdf reader thing
from dotenv import load_dotenv
import nltk

from .llm import get_embedding
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



load_dotenv()


def ingest_pdf():
    """ingests the pdf text"""
    pdf_path = os.getenv("PDF_PATH")

    
    for f in os.listdir(pdf_path):
        text = ""
        doc = fitz.open(
            f"{pdf_path}{f}"
        )  # TODO: we want to update db row to be per doc ? or per page idk
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text")
        process_pdf(text)


def chunk(tokens: list, chunk_size: int, overlap_size: int) -> list[str]:
    """ choose a chunk, breaks up text into chunks and returns a list of chunks"""
    if len(tokens) <= chunk_size:
        return " ".join(tokens)

    start, end = 0, chunk_size
    chunks = []
    while end < len(text):
        chunks.append(" ".join(tokens[start:end]))
        start = end - overlap_size 
        end = start + chunk_size

    return chunks 


def process_pdf(text: str, chunk_size: int = 200, overlap_size: int = 0, model: str = "nomic-embed-text", sentence_transformer: bool = True) -> None:
    """ process text. 
        Adjust the chunksize and overlap :))  for yeah
    """
    nltk.download('punkt_tab')
    stop_words = set(stopwords.words('english'))

    # clean & 
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [tok for tok in tokens if tok not in stopwords] # lol
    
    chunks = chunk(tokens, chunk_size, overlap_size) 

    embedding = get_embedding(text, model, sentence_transformer) # vectorize 
    # TODO: generate 5 different embeddings per each document, just store them as attr in the db
    return embedding # testing


def remove_stop(text):
    pass




print(ingest_pdf())

import os

import fitz  # pdf reader thing
from dotenv import load_dotenv
import nltk

from .llm import get_embedding
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



load_dotenv()


def ingest_pdf(dct: dict):
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
        embeddings, chunks = process_pdf(text = text, *dct)
        add_to_db(dct["model"])

    return embeddings, chunks

def chunk(tokens: list, chunk_size: int, overlap_size: int) -> list[str]:
    """ choose a chunk, breaks up text into chunks and returns a list of chunks"""
    if len(tokens) <= chunk_size:
        return " ".join(tokens)

    start, end = 0, chunk_size
    chunks = []
    while end < len(tokens):
        chunks.append(" ".join(tokens[start:end]))
        start = end - overlap_size 
        end = start + chunk_size

    return chunks 


def process_pdf(text: str, chunk_size: int = 200, overlap_size: int = 0, model: str = "nomic-embed-text", sentence_transformer: bool = True) -> list:
    """ process text. 
        Adjust the chunksize and overlap :))  for yeah
    """
    nltk.download('punkt_tab')
    stop_words = set(stopwords.words('english'))

    # clean & 
    text = text.lower()
    talk_tuah = word_tokenize(text)
    tokens = [tauk for tauk in talk_tuah if tauk not in stopwords] # lol
    
    chunks = chunk(tokens, chunk_size, overlap_size) 

    embeddings = []
    for chunk in chunks: 
        embeddings.append(get_embedding(chunk, model, sentence_transformer)) # vectorize & append
        
    # TODO: generate 3 different embeddings per each document, just store them as attr in the db
    return embeddings, chunks # testing

def add_to_db(add_func, pdf_title:str, text: str, overlap_size: int,  embedding: list, model: str, start: int, end: int): 
    for embed in embedding: 
        add_func(pdf_title, text, overlap_size, embed, model, start, end)

# postgres, redis, chroma


def main():
    
    pass

main()

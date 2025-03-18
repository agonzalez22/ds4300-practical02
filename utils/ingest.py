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


def chunk(text, size: int = 100, overlap_size: int = 0):
    """ choose a chunk, breaks up text into chunks and returns a list of chunks"""
     
    pass

def process_pdf(text):
    """process text"""
    nltk.download('punkt_tab')
    stop_words = set(stopwords.words('english'))

    # clean
    text = text.lower()
    toks = word_tokenize(text)
    toks = [tok for tok in toks if tok not in stopwords]
    print(toks)

    # tokenize 
    #embedding = get_embedding(text, 'all-MiniLM-L6-v2')  # vectorize
    embedding = get_embedding(text, sentence_transformer=False)
    # TODO: generate 5 different embeddings per each document, just store them as attr in the db
    return embedding # testing


def remove_stop(text):
    pass




print(ingest_pdf())

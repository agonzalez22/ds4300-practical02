import os

import fitz  # pdf reader thing
from dotenv import load_dotenv
import nltk

from llm import get_embedding
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# nltk.download('stopwords')

load_dotenv()

class PDF: 
    def __init__(self, pdf_path): 
        self.pdf_path = pdf_path
        self.title = ""
        self.chunk_size = 200
        self.overlap_size = 0
        self. embeddings = []
        self.chunks = []
        self.model = "nomic-embed-text" 
        self.text = ""

    def read_pdf(self): 
        """ reads the pdf"""
        doc = fitz.open(self.pdf_path)
        self.title = doc.metadata.get("title", "No title available")
        for page_num in range(len(doc)): 
            self.text += doc.load_page(page_num).get_text('text')
        print(f"Finished reading {self.title}")
    
    def chunk(self, tokens: list) -> list[str]:
        """ choose a chunk, breaks up text into chunks and returns a list of chunks"""
        if len(tokens) <= self.chunk_size:
            return " ".join(tokens)

        start, end = 0, self.chunk_size
        chunks = []
        while end < len(tokens):
            chunks.append(" ".join(tokens[start:end]))
            start = end - self.overlap_size 
            end = start + self.chunk_size

        return chunks 
    
    def process(self, chunk_size=200, overlap_size=0, model="nomic-embed-text"): 
        """ process the pdf and prepare for embedding"""
        # read the pdf to update the text ;0
        self.read_pdf()

        # also update these attributes for later 
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.model = model

        stop_words = set(stopwords.words('english'))

        # clean & tokenize
        self.text = self.text.lower()
        talk_tuah = word_tokenize(self.text)
        tokens = [tauk for tauk in talk_tuah if tauk not in stop_words] # lol

        # chunk based on the chunk_size
        self.chunks = self.chunk(tokens) 

        for c in self.chunks: 
            self.embeddings.append(get_embedding(c, self.model)) # vectorize & append
            
    
    def ingest(self, func): 
        """ ingests the data into whichever db using whichever function necessary. If chroma, do something different. """
        for i in range(len(self.chunks)): 
            func(self.pdf_title, self.chunks[i], self.overlap_size, self.embeddings[i], self.model, self.start[i], self.end[i])

def main():
     # TODO: generate 3 different embeddings per each document, just store them as attr in the db

    folder = os.getenv("PDF_PATH")
    print("Starting...")
    # run this to process all the text. 
    for f in os.listdir(os.getenv("PDF_PATH")): 
        curr_pdf = PDF(f"{folder}{f}")
        curr_pdf.process(chunk_size=200, overlap_size=0, model="nomic-embed-text")
        print(curr_pdf.embeddings)
        print(len(curr_pdf.embeddings))
        # run this to send up to db 
        # curr_pdf.ingest(func) # modify this to be whatever we want 

main()

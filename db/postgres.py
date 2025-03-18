import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def connect():
    """ connect to the db, returns connection obj 
        
        * if connection is closed: 0, that means connection is OPEN 
    """
    conn = psycopg2.connect(database="postgres", # leave hardcoded? 
                            host="localhost",
                            user="postgres",
                            password=os.getenv("POSTGRES_PASS"),
                            port="5432")
    return conn

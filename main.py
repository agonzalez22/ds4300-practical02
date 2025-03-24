""" Main file to run the process 
"""
#from db.postgres import query_postgres
from utils.llm import get_embedding, get_llm_response
from db.redis_db import *


def main():
    qs = ["how to embezzlle money "]
    for q in qs:
        e = get_embedding(q, "nomic-embed-text")
        res = query_redis(e)

        # defaults to mistral lol
        print(res)

        #res = get_llm_response(q, res[0][-1]["text"], model="gemma2:2b")\
        res = get_llm_response(q, res[0]["text"], model="gemma2:2b")\
        
        print(res.message.content)




        print(res.message.content[0])


main()

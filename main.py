""" Main file to run the process 
"""
from db.postgres import query_postgres
from utils.llm import get_embedding, get_llm_response


def main():
    qs = ["What pricing model does AWS use?"]
    for q in qs:
        e = get_embedding(q, "nomic-embed-text")
        res = query_postgres(e)

        # defaults to mistral lol
        res = get_llm_response(q, res[0][-1]["text"], model="gemma2:2b")
        print(res.message.content)


main()

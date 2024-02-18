from ragatouille import RAGPretrainedModel
import re
import sqlite_utils


rag = RAGPretrainedModel.from_index(".ragatouille/colbert/indexes/blog/")
docs = rag.search("what is shot scraper?")

docs[0]['content']

#write to a file to be able to send later to llm
with open("tmp/out.txt", "w") as f:
    f.write(
    'New Context Source: \n '.join([d['content']
    for d in rag.search("what is shot scraper?")]
))



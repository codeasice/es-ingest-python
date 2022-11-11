import uuid
from elasticsearch import Elasticsearch
import os
import tika
tika.initVM()
from tika import parser
import re
import sys

# USAGE: query.py [keyword] [elasticsearch index]

es_server = "http://localhost:9200"

num_args = len(sys.argv)

# KEYWORD
if num_args > 1: 
    keyword = str(sys.argv[1])
else: 
    keyword = "architect"

# ELASTIC SEARCH INEX
if num_args > 2:
    es_index = str(sys.argv[2])
else: 
    es_index = "es-ingest"

print("Connecting to Elasticsearch")
client = Elasticsearch(hosts=[es_server],verify_certs=False)

print(f"Search for: {keyword}")
q = {
    'size' : 1000,         
    "query": {
        "match": {
             "content": keyword
         }
  }}
resp = client.search(index=es_index, query={"match": {"content": keyword}}, size = 1000)
num_results = resp['hits']['total']['value']
i=0
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    i = i+1
    id = hit["_id"]
    text = hit["_source"]["content"]
    filename = hit["_source"]["filename"]
    print (f"----------- Searching doc ({i} / {num_results})[{id}] - {filename}")
    
    # Grab n words before and after the keyword
    n = 5
    word = r"\W*([\w]+)"
    for res in re.findall(r'{}\W*{}{}'.format(word*n,keyword,word*n), text, re.IGNORECASE):
        print(f"{' '.join(res[:n])} {keyword} {' '.join(res[n:])}")

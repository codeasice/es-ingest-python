import uuid
from elasticsearch import Elasticsearch
import os
import tika
tika.initVM()
from tika import parser
import sys

# USAGE: ingest.py [directory] [elasticsearch index]

es_server = "http://localhost:9200"

# DIRECTORY
if num_args > 1: 
    directory = str(sys.argv[1])
else: 
    directory = '/Users/clambert/Downloads/fish_documents/'

# ELASTIC SEARCH INEX
if num_args > 2:
    es_index_name = str(sys.argv[2])
else: 
    es_index_name = 'fishy'

print("Connecting to Elasticsearch")
client = Elasticsearch(hosts=[es_server], verify_certs=False)

#----------------DROP INDEX
print("Dropping Index")
try:
    client.indices.delete(index=es_index_name)
except: 
    print("Failed to drop - hopefully that's ok")

#---------------LIST INDEX
print("Listing Indices")
resp = client.indices.get_alias().keys()

print(str(resp))
#---------------CREATE INDEX
request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    'mappings': {
        'properties': {
            'metadata': {'type': 'text'},
            'filename': {'type': 'text'},
            'content': {'type': 'text'},
            'body': {'type': 'text'}
        }}
}
print("Creating Index")
client.indices.create(index = es_index_name, body = request_body)

#----------- Ingest all the docs
i = 0
for filename in os.listdir(directory):
   f = os.path.join(directory, filename)
   # checking if it is a file
   if os.path.isfile(f):
        i = i+1
        id = uuid.uuid4()
        print(f"IMPORTING FILE {i} to ID {id}: {f}")
        parsed = parser.from_file(f)
        client.index(
            index=es_index_name,
            document={
            'id': id,
            'filename': f, 
            'content': parsed["content"]
            })
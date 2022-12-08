import uuid
from elasticsearch import Elasticsearch
import os
import tika
tika.initVM()
from tika import parser
import re
import sys
import stopit
from settings import Settings
import ntpath


header_text = r'''
   ___                    
  / _ \ _  _ ___ _ _ _  _ 
 | (_) | || / -_) '_| || |
  \__\_\\_,_\___|_|  \_, |
                      |__/ 
'''
print(header_text)

data_folder = os.path.join(".")
file_to_open = os.path.join(data_folder, "settings.json")
settings = Settings().load_or_default_config()

es_server = settings.get_setting("es_server", default="http://localhost:9200")
print(f"es_server={es_server}")

max_documents = settings.get_setting("max_documents", default=1000)
print(f"max_documents={max_documents}")

num_surrounding_words = settings.get_setting("num_surrounding_words", default=4)
print(f"num_surrounding_words={num_surrounding_words}")

filenames_to_skip = settings.get_setting("filenames_to_skip", default=[])
print(f"filenames_to_skip={filenames_to_skip}")


# USAGE: query.py [keyword] [elasticsearch index]
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
    es_index = settings.get_setting("es_index", default="fishy")

def forever_search(keyword, text):
    # Grab n words before and after the keyword
    word = r"\W*([\w]+)"
    for res in re.findall(r'{}\W*{}{}'.format(word*num_surrounding_words,keyword,word*num_surrounding_words), text, re.IGNORECASE):
        print(f"{' '.join(res[:num_surrounding_words])} {keyword} {' '.join(res[num_surrounding_words:])}")

# https://stackoverflow.com/a/8384788
# Grab filename from path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

print("Connecting to Elasticsearch")
client = Elasticsearch(hosts=[es_server],verify_certs=False)

print(f"Search for: {keyword}")
q = {
    'size' : max_documents,         
    "query": {
        "match": {
             "content": keyword
         }
  }}
resp = client.search(index=es_index, query={"match": {"content": keyword}}, size = max_documents)
num_results = resp['hits']['total']['value']
i=0
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    i = i+1
    id = hit["_id"]
    text = hit["_source"]["content"]
    filename = hit["_source"]["filename"]

    if num_surrounding_words==0:
        print (f"{filename}")
    else:
        print (" ")
        if path_leaf(filename) in filenames_to_skip:
            print (f"----------- SKIPPING doc ({i} / {num_results})[{id}] - {filename}")
        else: 
            print (f"----------- Searching doc ({i} / {num_results})[{id}] - {filename}")
            forever_search(keyword, text)

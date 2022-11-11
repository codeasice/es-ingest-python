# OVERVIEW
Quick & dirty python scripts to ingest PDF, DOC, etc... file into elasticsearch using Tika for text extraction

# INGEST
USAGE: ingest.py [directory] [elasticsearch index]

Ingests text from all files located in the directory into the specified index

# QUERY
USAGE: query.py [keyword] [elasticsearch index]

Searches for the keyword in the specified index and returns all matches including a few words before and after the keyword

# REFERENCE NOTES
https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

C:\Users\clambert>curl -X PUT "localhost:9200/es-index?pretty"
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "es-index"
}

curl -X GET "localhost:9200/es-index/_search?pretty"
curl -X DELETE "localhost:9200/es-ingest?pretty"

curl -X PUT "localhost:9200/es-index?pretty" -H 'Content-Type: application/json' -d'
{  "settings": {
"number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "content": { "type": "text" }
      "body": { "type": "text" }
    }
  }
}
'

http://localhost:9200/es-ingest/_search?q=browser
# OVERVIEW
Quick & dirty python scripts to ingest PDF, DOC, etc... file into elasticsearch using Tika for text extraction

# INGEST
USAGE: ingest.py [directory] [elasticsearch index]

Ingests text from all files located in the directory into the specified index

# QUERY
USAGE: query.py [keyword] [elasticsearch index]

Searches for the keyword in the specified index and returns all matches including a few words before and after the keyword

# FEATURES
## Settings
settings.json contains several settings that can be configured

## Skip Files
"filenames_to_skip" is an array in the settings.json files can contain a list of files to skip (paths are stripped if they are included)
This can be used to ignore irrelevant or bad files (Sometimes regex gets hung due to well-known bugs)

# REFERENCE NOTES
https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

http://localhost:9200/_aliases?pretty=true

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

docker-compose ERROR: bootstrap checks failed | max > virtual memory areas vm.max_map_count [65530] is too low, increase to > at least [262144]
open power shell 
wsl.exe -u root
sysctl -w vm.max_map_count=262144
exit

docker exec -u 0 -it es01 bash
apt-get update
apt-get install vim
vim /usr/share/elasticsearch/config/elasticsearch.yml
:colorscheme desert

 docker run -e ES_JAVA_OPTS="-Xms1g -Xmx1g" --name es02 -p 9201:9200  -p 9300:9300 -it docker.elastic.co/elasticsearch/elasticsearch:8.5.1
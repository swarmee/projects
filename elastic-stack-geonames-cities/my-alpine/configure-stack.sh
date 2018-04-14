#!/bin/bash

# Wait for Elasticsearch to start up before doing anything.
until curl -s http://elasticsearch1:9200/_cat/health -o /dev/null; do
    echo Waiting for Elasticsearch...
    sleep 1
done


# Wait for Kibana to start up before doing anything.
##until curl -s http://kibana1:5601/login -o /dev/null; do
##    echo Waiting for Kibana...
##    sleep 1
##done

# Set Templates typeAhead
curl -s -H 'Content-Type: application/json'  -XPOST http://elasticsearch1:9200/_scripts/typeAhead -d '{ "script": { "lang": "mustache", "source": { "suggest": { "asciiName-suggestion": { "prefix": "{{typeAheadText}}", "completion": { "field": "asciiName-suggestion", "fuzzy": { "fuzziness": 0, "prefix_length": 3 }, "skip_duplicates": true } }, "alternateNames-suggestion": { "prefix": "{{typeAheadText}}", "completion": { "field": "alternateNames-suggestion", "fuzzy": { "fuzziness": 0, "prefix_length": 3 }, "skip_duplicates": true } } } } } }'

# Set Template nearGeoNameId
curl -s -H 'Content-Type: application/json'  -XPOST http://elasticsearch1:9200/_scripts/nearGeoNameId -d '{  "script": { "lang": "mustache","source": {  "query": { "bool": {    "must": { "geo_distance": {  "distance": "{{distance}}",  "location": {   "lat": "{{lat}}",   "lon": "{{lon}}"}  }   } }  }, "size" :100 } }}'

echo 'Templates all loaded up'
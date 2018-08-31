#!/bin/bash

# Wait for Elasticsearch to start up before doing anything.
until curl -s http://elasticsearch:9200/_cat/health -o /dev/null; do
    echo Waiting for Elasticsearch...
    sleep 10
done


# Wait for Kibana to start up before doing anything.
until curl -s http://kibana:5601/login -o /dev/null; do
    echo Waiting for Kibana...
    sleep 10
done


# load mapping
curl -H 'Content-Type: application/json' -XPUT 'http://elasticsearch:9200/real-estate-sales?pretty' -d @/tmp/sample/real-estate-sales.mapping.json

# load data
curl -H 'Content-Type: application/x-ndjson' -XPOST 'http://elasticsearch:9200/real-estate-sales/sales/_bulk?pretty' --data-binary @/tmp/sample/real-estate-sales.sample.data.json

echo 'Templates all loaded up'

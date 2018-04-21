#!/bin/bash

# Wait for Elasticsearch to start up before doing anything.
until curl -s http://elasticsearch1:9200/_cat/health -o /dev/null; do
    echo Waiting for Elasticsearch...
    sleep 1
done


# Wait for Kibana to start up before doing anything.
until curl -s http://kibana1:5601/login -o /dev/null; do
    echo Waiting for Kibana...
    sleep 1
done

# Set the default index pattern.
#curl -H 'Content-Type: application/json' -s -XPUT http://elasticsearch1:9200/.kibana/doc/6.2.3 \
#     -d "{\"defaultIndex\" : \"filebeats*\"}"


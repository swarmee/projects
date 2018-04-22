#!/bin/bash


# Wait for Elasticsearch to start up before doing anything.
until curl -s http://localhost:9200/_cat/health -o /dev/null; do
    echo Waiting for Elasticsearch...
    sleep 1
done

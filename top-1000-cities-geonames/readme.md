# Docker Compose to Bring Up Elastic Stack and load ~100,000 Geoname Cities

## Start the Full Stack on single host

```docker-compose up```

This will download all the images (nginx, logstash, elastic, python), loads the geonames data (using logstash with a preconfigured 'mapping' for type ahead suggestion on city name and alternative city name), publishes two simple search templates, and boot up a simple swagger test page that allows you to test the search templates. 

## Where to find the swagger UI

The swagger ui can be found on port 80

So ```http://localhost``` in your browser should bring up the swagger interface. 


## Loading Data and Applying Search Templates to Existing Elastic Search instance

So you have an existing elasticsearch cluster, how do you load up this data and templates into your existing cluster. The steps required are;

###1. Update the elasticsearch host and port variables in the standalone ```standalone-logstash-docker-compose.yml``` file. I.e. change the below variables to what every you want them to be. 

    environment:
      ELASTICSEARCH_HOST: elasticsearch1
      ELASTICSEARCH_PORT: 9200

###2. Then run the standalone logstash docker compose file. This should push all the data into your cluster. 

```docker-compose -f standalone-logstash-docker-compose.yml up```


###3. Publish the search templates 

Post in Completion Suggestion Template

```curl -s -H 'Content-Type: application/json'  -XPOST http://<YOUR HOST HERE>:9200/_scripts/typeAhead -d '{ "script": { "lang": "mustache", "source": { "suggest": { "asciiName-suggestion": { "prefix": "{{typeAheadText}}", "completion": { "field": "asciiName-suggestion", "fuzzy": { "fuzziness": 0, "prefix_length": 3 }, "skip_duplicates": true } }, "alternateNames-suggestion": { "prefix": "{{typeAheadText}}", "completion": { "field": "alternateNames-suggestion", "fuzzy": { "fuzziness": 0, "prefix_length": 3 }, "skip_duplicates": true } } } } } }' ```

Post in Geo Distance Template

```curl -s -H 'Content-Type: application/json'  -XPOST http://<YOUR HOST HERE>:9200/_scripts/nearGeoNameId -d '{  "script": { "lang": "mustache","source": {  "query": { "bool": {"must": {"geo_distance": { "distance": "{{distance}}","location": {   "lat": "{{lat}}", "lon": "{{lon}}"}}}}}, "size" :100 } }}' ```

###4. Test out the Search Templates

Type Ahead Search Template - Test
```curl -s -H 'Content-Type: application/json'  -XPOST http://<YOUR HOST HERE>:9200/city/_search/template -d '{"id": "typeAhead" ,"params": {"typeAheadText": "sydn"}}' | python -m json.tool ```

Cities Near a specific Lat / Lon
```curl -s -H 'Content-Type: application/json'  -XPOST http://<YOUR HOST HERE>:9200/city/_search/template -d '{"id": "nearGeoNameId" ,"params": {"lon": 0, "lat": 0, "distance" : "1000km" }}' | python -m json.tool ```

In the swagger test page we accept a geoNameId then find its Lat / Lon and then submit a search to the above template. There is no way to perform this type of request in a single request. 

## Sundry Information

More details on the completion suggestion can be found here --> https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters-completion.html

The GeoNames geographical data used in this repo is available for download free of charge under a creative commons attribution license. Further details can be found here --> http://www.geonames.org/about.html

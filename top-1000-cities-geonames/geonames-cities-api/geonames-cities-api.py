from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify
from elasticsearch import Elasticsearch
import json

### Setup elastic search connection
es_host = {"host": "elasticsearch1", "port": 9200}
es = Elasticsearch([es_host], retry_on_timeout=True, maxsize=25)

### ADD Near GeoName Id Template
#nearGeoNameIdTemplateBody = {  "script": { "lang": "mustache","source": {  "query": { "bool": {    "must": { "geo_distance": {  "distance": "{{distance}}",  "location": {   "lat": "{{lat}}",   "lon": "{{lon}}"}  }   } }  }, "size" :100 } }}
#addNearGeoNameIdTemplate = client.put_template(id='nearGeoNameId', body=nearGeoNameIdTemplateBody)
#elasticsearch.put_template(id='nearGeoNameId', body=nearGeoNameIdTemplateBody)
#print(addNearGeoNameIdTemplate)

### ADD Type Ahead Template
#typeAheadTemplateBody = ({ "script": { "lang": "mustache", "source": { "suggest": { "asciiName-suggestion": { "prefix": "{{typeAheadText}}", "completion": { "field": "asciiName-suggestion", "fuzzy": { "fuzziness": 0, "prefix_length": 3 }, "skip_duplicates": true } }, "alternateNames-suggestion": { "prefix": "{{typeAheadText}}", "completion": { "field": "alternateNames-suggestion", "fuzzy": { "fuzziness": 0, "prefix_length": 3 }, "skip_duplicates": true } } } } } })
#addTypeAheadTemplate = es.put_template(id='typeAhead', body=typeAheadTemplateBody)
#print(addTypeAheadTemplate)

app = Flask(__name__)
api = Api(app,
	      version='1.0', 
          title='Swagger Test Page for Elasticsearch \"Geoname Data\" Search Templates', 
          description='Test Page for \"Geoname Data\" Searches', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="www.swarmee.net"
         )
app.wsgi_app = ProxyFix(app.wsgi_app)

ns = api.namespace('city', description='Simple Endpoints to Test Elastic API operations')

query1 = api.model('query1', {
    'typeAheadText': fields.String(default='Syd', required=True, description='Type Ahead Text'),
    'typeAheadTemplate': fields.String(default='typeAhead', required=True, description='Template for Type Ahead'),
    })

query2 = api.model('query2', {
    'nearGeoNameId': fields.String(default='2293507', required=True, description='Search For Cities Near This GeoNameId'),
    'nearGeoNameIdDistance': fields.String(default='100km', required=True, description='Distance From City to Include in results')   
    })

@ns.route('/typeAhead')
class typeAhead(Resource):
    @ns.expect(query1)
    def post(self):
        typeAheadText = api.payload['typeAheadText']
        typeAheadTemplate = api.payload['typeAheadTemplate']
        abc = {'id': typeAheadTemplate ,'params': {'typeAheadText': typeAheadText}}
        resp = es.search_template(index="city", body=abc, filter_path=['suggest.*suggestion.options.text','suggest.*suggestion.options._id'])
        return jsonify(resp)  

@ns.route('/typeAhead/Full')
class typeAheadFull(Resource):
    @ns.expect(query1)
    def post(self):
        typeAheadText = api.payload['typeAheadText']
        typeAheadTemplate = api.payload['typeAheadTemplate']
        abc = {'id': typeAheadTemplate ,'params': {'typeAheadText': typeAheadText}}
        resp = es.search_template(index="city", body=abc)
##        resp['matches'] = resp.pop('hits')        
##        print(resp)
        return jsonify(resp)

#### General search of geoname data using search term

@ns.route('/search/<searchTerms>')
class productSearch(Resource):
    def get(self, searchTerms):
        simpleSearchResponse = es.search(index="city", body="{\"query\": {\"simple_query_string\": {\"query\": \"%s\"}}}" % searchTerms)
        return jsonify(simpleSearchResponse)       

#### Search geoname data by geonameId

@ns.route('/search/<geonameId>')
class geonameIdSearch(Resource):
    def get(self, geonameId):
        geonameIdSearchResponse = es.search(index="city", body="{\"query\": {\"match\": {\"_id\": \"%s\"}}}" % geonameId)
        return jsonify(geonameIdSearchResponse)       


#### finds records near specific geo point - based on supplied distance ####

@ns.route('/search/NearGeoNameId')
class nearGeonameId(Resource):
    @ns.expect(query2)
    def post(self):
        nearGeoNameId = api.payload['nearGeoNameId']
        nearGeoNameIdDistance = api.payload['nearGeoNameIdDistance']
        nearGeonameIdSearchResponse = es.search(index="city", body="{\"query\": {\"match\": {\"_id\": \"%s\"}}}" % nearGeoNameId, filter_path=['hits.hits._source.location.*'])
        for row in nearGeonameIdSearchResponse["hits"]["hits"]:
          getLatLon = row["_source"]["location"]
        lon = getLatLon['lon']
        lat = getLatLon['lat']
        abc = {'id': 'nearGeoNameId' ,'params': {'lon': lon, 'lat': lat, 'distance' : nearGeoNameIdDistance }}
        resp3 = es.search_template(index="city", body=abc, filter_path=['hits.total', 'hits.hits._source.asciiName', 'hits.hits._source.location', 'hits.hits._source.geonameId'])
#        finalResponse = []
#        for row in resp3["hits"]["hits"]:
#          finalResponse.append(row["_source"])
        return jsonify(resp3)       


#### counts the number of city records stored in elastic ####
@ns.route('/count')
class geoname(Resource):
    def get(self):
        resp = es.count(index="city", filter_path=['-took','-timed_out','-_shards'])
        return resp

#### provides indication if the elastic backend is healthy ####
@ns.route('/backEndHealth')
class backEndHealth(Resource):
    def get(self):
        resp = es.cluster.health(filter_path=['status'])
        return resp

if __name__ == '__main__':
    app.run(debug=True)

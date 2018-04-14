from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify
from elasticsearch import Elasticsearch
import json

### Setup elastic search connection
es_host = {"host": "elasticsearch1", "port": 9200}
es = Elasticsearch([es_host], retry_on_timeout=True, maxsize=25)

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

typeAheadParser = ns.parser()
typeAheadParser.add_argument('typeAheadText', type=str, help='Type Ahead Text', location='form')
typeAheadParser.add_argument('typeAheadTemplate', type=str, help='Template for Type Ahead', location='form')


nearGeoNameIdParser = ns.parser()
nearGeoNameIdParser.add_argument('nearGeoNameId', type=str, help='Search For Cities Near This GeoNameId', location='form')
nearGeoNameIdParser.add_argument('nearGeoNameIdDistance', type=str, help='Distance From City to Include in results', location='form')


#### finds records near specific geo point - based on supplied distance ####

@ns.route('/search/NearGeoNameId')
class nearGeonameId(Resource):
    @ns.doc(parser=nearGeoNameIdParser)    
    def post(self):
        args = typeAheadParser.parse_args()
        nearGeoNameId = args['nearGeoNameId']
        nearGeoNameIdDistance = args['nearGeoNameIdDistance']
        nearGeonameIdSearchResponse = es.search(index="city", body="{\"query\": {\"match\": {\"_id\": \"%s\"}}}" % nearGeoNameId, filter_path=['hits.hits._source.location.*'])
        for row in nearGeonameIdSearchResponse["hits"]["hits"]:
          getLatLon = row["_source"]["location"]
        lon = getLatLon['lon']
        lat = getLatLon['lat']
        abc = {'id': 'nearGeoNameId' ,'params': {'lon': lon, 'lat': lat, 'distance' : nearGeoNameIdDistance }}
        resp3 = es.search_template(index="city", body=abc, filter_path=['hits.total', 'hits.hits._source.asciiName', 'hits.hits._source.location', 'hits.hits._source.geonameId'])
        return jsonify(resp3)       

@ns.route('/typeAhead')
class typeAhead(Resource):
    @ns.doc(parser=typeAheadParser)
    def post(self):
        args = typeAheadParser.parse_args()
        typeAheadText = args['typeAheadText']
        typeAheadTemplate = args['typeAheadTemplate']
        abc = {'id': typeAheadTemplate ,'params': {'typeAheadText': typeAheadText}}
        resp = es.search_template(index="city", body=abc, filter_path=['suggest.*suggestion.options.text','suggest.*suggestion.options._id'])
        return jsonify(resp) 

@ns.route('/typeAhead/Full')
class typeAheadFull(Resource):
    @ns.doc(parser=typeAheadParser)
    def post(self):
        args = typeAheadParser.parse_args()
        typeAheadText = args['typeAheadText']
        typeAheadTemplate = args['typeAheadTemplate']
        abc = {'id': typeAheadTemplate ,'params': {'typeAheadText': typeAheadText}}
        resp = es.search_template(index="city", body=abc)
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
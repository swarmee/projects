from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify
from elasticsearch import Elasticsearch
import json


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

query1 = api.model('query1', {
    'typeAheadText': fields.String(default='abe', required=True, description='Type Ahead Text'),
    'typeAheadTemplate': fields.String(default='typeAhead', required=True, description='Template for Type Ahead'),
    })

@ns.route('/typeAhead')
class typeAhead(Resource):
    @ns.expect(query1)
    def post(self):
        typeAheadText = api.payload['typeAheadText']
        typeAheadTemplate = api.payload['typeAheadTemplate']
        abc = {'id': typeAheadTemplate ,'params': {'typeAheadText': typeAheadText}}
        resp = es.search_template(index="city", body=abc, filter_path=['-took','-timed_out','-hits', '-_shards'])
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

@ns.route('/<geonameId>')
class geonameIdSearch(Resource):
    def get(self, geonameId):
        geonameIdSearchResponse = es.search(index="city", body="{\"query\": {\"match\": {\"_id\": \"%s\"}}}" % geonameId)
        return jsonify(geonameIdSearchResponse)       


#### finds records near specific geo point - based on supplied distance ####

@ns.route('/near/<geonameId>')
class nearGeonameId(Resource):
    def get(self, geonameId):
        nearGeonameIdSearchResponse = es.search(index="city", body="{\"query\": {\"match\": {\"_id\": \"%s\"}}}" % geonameId, filter_path=['hits.hits._source.productName'])
#        for row in likeProductNumberSearchResponse["hits"]["hits"]:
#          likeProductNumberClientResponse = row["_source"]["productName"]
#        resp3 = es.search(index="products", body="{\"query\": { \"common\": {\"productName\": {\"query\": \"%s\",\"cutoff_frequency\": 0.1}}}}" % likeProductNumberClientResponse, filter_path=['hits.hits._source.*'])
#        finalResponse = []
#        for row in resp3["hits"]["hits"]:
#          finalResponse.append(row["_source"])
        return jsonify(nearGeonameIdSearchResponse)       


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

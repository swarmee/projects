from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify
from elasticsearch import Elasticsearch
import json


### Setup elastic search connection
es_host = {"host": "elasticsearch", "port": 9200}
es = Elasticsearch([es_host], retry_on_timeout=True, maxsize=25)


app = Flask(__name__)
api = Api(app,
        version='1.0', 
          title='Elasticsearch Backed Country API', 
          description='Data from from https://restcountries.eu/rest/v2/all', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="www.swarmee.net"
         )
app.wsgi_app = ProxyFix(app.wsgi_app)

ns = api.namespace('country', description='Country Namespace')

basicCountryQuery = ns.parser()
basicCountryQuery.add_argument('searchText', type=str, help='query string search text', location='form')


##### Use elastic query _string search to search country list
@ns.route('/basicsearch')
class basicsearch(Resource):
    @ns.doc(parser=basicCountryQuery)
    def post(self):
        args = basicCountryQuery.parse_args()
        searchText = args['searchText']
        inputQuery = {'query': { 'query_string' : {'query' :  searchText }}}
        interimResponse = es.search(index="countries", body=inputQuery)
        finalResponse = []
        for row in interimResponse["hits"]["hits"]:
          finalResponse.append(row["_source"])
        return jsonify(finalResponse)       

##### Count of Countries
@ns.route('/count')
class countryCount(Resource):
    def get(self):
        responseCount = es.count(index="countries", filter_path=['-took','-timed_out','-_shards'])
        return responseCount


##### Two Character Country Code Search
@ns.route('/twoCharacterCode/<twoCharacterCode>')
class twoCharacterCode(Resource):
    def get(self, twoCharacterCode):
        twoCharacterCodeInterimResponse = es.search(index="countries", body="{\"query\": {\"match\": {\"alpha2Code\": \"%s\"}}}" % twoCharacterCode)
        twoCharacterCodeFinalResponse = []
        for row in twoCharacterCodeInterimResponse["hits"]["hits"]:
          twoCharacterCodeFinalResponse.append(row["_source"])
        return jsonify(twoCharacterCodeFinalResponse)  

##### Three Character Country Code Search
@ns.route('/threeCharacterCode/<threeCharacterCode>')
class threeCharacterCode(Resource):
    def get(self, threeCharacterCode):
        threeCharacterCodeInterimResponse = es.search(index="countries", body="{\"query\": {\"match\": {\"alpha3Code\": \"%s\"}}}" % threeCharacterCode)
        threeCharacterCodeFinalResponse = []
        for row in threeCharacterCodeInterimResponse["hits"]["hits"]:
          threeCharacterCodeFinalResponse.append(row["_source"])
        return jsonify(threeCharacterCodeFinalResponse)  


if __name__ == '__main__':
    app.run(debug=False)

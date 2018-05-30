from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify, request
from elasticsearch import Elasticsearch
import json
#import logging
#from logging.handlers import RotatingFileHandler


### Setup elastic search connection
es_host = {"host": "localhost", "port": 9200}
es = Elasticsearch([es_host], retry_on_timeout=True, maxsize=25)

app = Flask(__name__)
api = Api(app,
        version='1.0', 
          title='Elasticsearch Backed Cities API', 
          description='Data from from https://geonames.org', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="www.swarmee.net"
         )
app.wsgi_app = ProxyFix(app.wsgi_app)


city_model = api.model("book", {
    "admin1Code": fields.String("Name of the book."),
    "admin2Code": fields.String("Name of the author."),
    "admin3Code": fields.String("Name of the book."),
    "admin4Code": fields.String("Name of the author.")
})


ns = api.namespace('city', description='City Namespace')

basicCityQuery = ns.parser()
basicCityQuery.add_argument('searchText', type=str, help='query string search text', location='form')


##### Use elastic query _string search to search city list
@ns.route('/basicsearch')
class basicsearch(Resource):
    @ns.doc(parser=basicCityQuery)
#    @api.marshal_with(city_model, envelope='data')
    def post(self):
        args = basicCityQuery.parse_args()
        searchText = args['searchText']
#        app.logger.info(searchText)
#        print(request.headers)
#        res = es.index(index="log", doc_type='_doc',  body={'searchText' : searchText})
#        test = request.headers['content-length']
#        res = es.index(index="log", doc_type='_doc',  body={'contentLength' : test , 'searchText' : searchText})
        inputQuery = {'query': { 'query_string' : {'query' :  searchText }}}
        interimResponse = es.search(index="city", body=inputQuery)
        finalResponse = []
        for row in interimResponse["hits"]["hits"]:
          finalResponse.append(row["_source"])
        return jsonify(finalResponse)   
        

##### Count of Countries
@ns.route('/count')
class cityCount(Resource):
    def get(self):
        responseCount = es.count(index="city", filter_path=['-took','-timed_out','-_shards'])
        return responseCount


##### Two Character City Code Search
@ns.route('/twoCharacterCode/<twoCharacterCode>')
class twoCharacterCode(Resource):
    def get(self, twoCharacterCode):
        twoCharacterCodeInterimResponse = es.search(index="city", body="{\"query\": {\"match\": {\"countryCode\": \"%s\"}}}" % twoCharacterCode)
        twoCharacterCodeFinalResponse = []
        for row in twoCharacterCodeInterimResponse["hits"]["hits"]:
          twoCharacterCodeFinalResponse.append(row["_source"])
        return jsonify(twoCharacterCodeFinalResponse)  


if __name__ == '__main__':
#    handler = RotatingFileHandler('/tmp/foo.log', maxBytes=10000, backupCount=1)
#    handler.setLevel(logging.INFO)
#    app.logger.addHandler(handler)
    app.run(debug=True)

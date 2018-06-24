from flask_restplus import Api, Resource, fields, reqparse
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify
from elasticsearch import Elasticsearch
import json


es_host = {"host": "localhost", "port": 9200}
es = Elasticsearch([es_host], retry_on_timeout=True, maxsize=25)

app = Flask(__name__)
api = Api(app,
	      version='1.0', 
          title='Get Product And \"like\" Product Details', 
          description='Simple Product API Endpoints', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="www.swarmee.net"
         )
app.wsgi_app = ProxyFix(app.wsgi_app)
ns = api.namespace('product', description='Simple Product API operations')


query1 = api.model('query1', {
    'searchText': fields.String(default='Syd', required=True, description='searchText')
    })

@ns.route('/search/<searchTerms>')
class productSearch(Resource):
    def get(self, searchTerms):
        productSearchResponse = es.search(index="products", body="{\"query\": {\"query_string\": {\"query\": \"%s\"}}}" % searchTerms)
        hits = productSearchResponse["hits"]["total"]
        productSearchClientResponse = []
        for row in productSearchResponse["hits"]["hits"]:
          productSearchClientResponse.append(row["_source"])
        return productSearchClientResponse, 200, {'X-total-hits' : hits}

@ns.route('/search')
class typeAhead(Resource):
    @ns.expect(query1)
    def post(self):
        searchText = api.payload['searchText']
        productSearchResponse = es.search(index="products", body="{\"query\": {\"query_string\": {\"query\": \"%s\"}}}" % searchText)
        hits = productSearchResponse["hits"]["total"]
        productSearchClientResponse = []
        for row in productSearchResponse["hits"]["hits"]:
          productSearchClientResponse.append(row["_source"])
        return productSearchClientResponse, 200, {'X-total-hits' : hits}


if __name__ == '__main__':
    app.run(debug=True)









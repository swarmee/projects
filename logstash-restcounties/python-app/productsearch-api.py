from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify
from elasticsearch import Elasticsearch

es_host = {"host": "elasticsearch1", "port": 9200}
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

@ns.route('/search/<searchTerms>')
class productSearch(Resource):
    def get(self, searchTerms):
        productSearchResponse = es.search(index="products", body="{\"query\": {\"query_string\": {\"query\": \"%s\"}}}" % searchTerms)
        productSearchClientResponse = []
        for row in productSearchResponse["hits"]["hits"]:
          productSearchClientResponse.append(row["_source"])
        return jsonify(productSearchClientResponse)       

@ns.route('/<productNumber>')
class productNumber(Resource):
    def get(self, productNumber):
        productNumberSearchResponse = es.search(index="products", body="{\"query\": {\"match\": {\"_id\": \"%s\"}}}" % productNumber)
        productNumberClientResponse = []
        for row in productNumberSearchResponse["hits"]["hits"]:
          productNumberClientResponse.append(row["_source"])
        return jsonify(productNumberClientResponse)       

@ns.route('/like/<productNumber>')
class likeProductNumber(Resource):
    def get(self, productNumber):
        likeProductNumberSearchResponse = es.search(index="products", body="{\"query\": {\"match\": {\"_id\": \"%s\"}}}" % productNumber, filter_path=['hits.hits._source.productName'])
        for row in likeProductNumberSearchResponse["hits"]["hits"]:
          likeProductNumberClientResponse = row["_source"]["productName"]
        resp3 = es.search(index="products", body="{\"query\": { \"common\": {\"street\": {\"query\": \"%s\",\"cutoff_frequency\": 0.1}}}}" % likeProductNumberClientResponse, filter_path=['hits.hits._source.*'])
        finalResponse = []
        for row in resp3["hits"]["hits"]:
          finalResponse.append(row["_source"])
        return jsonify(finalResponse)       

@ns.route('/count')
class productCount(Resource):
    def get(self):
        resp = es.count(index="products", filter_path=['-took','-timed_out','-_shards'])
        return resp

@ns.route('/health')
class elasticHealth(Resource):
    def get(self):
        resp = es.cluster.health(filter_path=['status'])
        return resp

if __name__ == '__main__':
    app.run(debug=True)

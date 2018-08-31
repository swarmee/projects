from flask_restplus import Api, Resource
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, jsonify
import requests
import urllib3
urllib3.disable_warnings()

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

host = 'elasticsearch'
requestHeaders = {'user-agent': 'my-python-app/0.0.1', 'content-type': 'application/json'}
requestURL = 'http://%s:9200/real-estate-sales/_search' % (host)

def populateJson(search_term):
    return  {
            "query": {
                "query_string" : {
                    "query": search_term 
                }
            }
            }

@ns.route('/search/<searchTerms>')
class documentSearch(Resource):
    def get(self, searchTerms):
        requestBody = populateJson(searchTerms)
        r = requests.get(requestURL,
                         auth=('test','test'),
                         json=requestBody,
                         headers=requestHeaders,
                          verify=False)
        r = r.json()
        return r       

@ns.route('/count')
class documentCount(Resource):
    def get(self):
        r = requests.get(requestURL,auth=('test','test'),headers=requestHeaders, verify=False)
        r = r.json() 
        return r["hits"]["total"]

if __name__ == '__main__':
    app.run(debug=True)






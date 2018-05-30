from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify, request
from elasticsearch import Elasticsearch
import probablepeople as pp
import json
from postal.parser import parse_address

### Setup elastic search connection
es_host = {"host": "elasticsearch", "port": 9200}
es = Elasticsearch([es_host], retry_on_timeout=True, maxsize=25)


app = Flask(__name__)
api = Api(app,
        version='1.0', 
          title='Name and Address Parsing and Related Elasticsearch Backed API', 
          description='Data from from https://geonames.org and restcountries.org', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="www.swarmee.net"
         )
app.wsgi_app = ProxyFix(app.wsgi_app)

#########################################################################
ns = api.namespace('city', description='City Namespace')
basicCityQuery = ns.parser()
basicCityQuery.add_argument('searchText', type=str, help='query string search text', location='form')

pns = api.namespace('partyType', description='Simple Party Parser and Typer')
partyName = pns.parser()
partyName.add_argument('partyName', type=str, help='partyName for Processing', location='form')

ans = api.namespace('addressParser', description='Simple Party Type Identification')
addressText = ans.parser()
addressText.add_argument('addressText', type=str, help='The address to be parsed into components', location='form')


cns = api.namespace('country', description='Country Namespace')
basicCountryQuery = cns.parser()
basicCountryQuery.add_argument('searchText', type=str, help='query string search text', location='form')

#########################################################################

##### Use elastic query _string search to search country list
@cns.route('/basicsearch')
class basicsearch(Resource):
    @cns.doc(parser=basicCountryQuery)
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
@cns.route('/count')
class countryCount(Resource):
    def get(self):
        responseCount = es.count(index="countries", filter_path=['-took','-timed_out','-_shards'])
        return responseCount


##### Two Character Country Code Search
@cns.route('/twoCharacterCode/<twoCharacterCode>')
class twoCharacterCode(Resource):
    def get(self, twoCharacterCode):
        twoCharacterCodeInterimResponse = es.search(index="countries", body="{\"query\": {\"match\": {\"alpha2Code\": \"%s\"}}}" % twoCharacterCode)
        twoCharacterCodeFinalResponse = []
        for row in twoCharacterCodeInterimResponse["hits"]["hits"]:
          twoCharacterCodeFinalResponse.append(row["_source"])
        return jsonify(twoCharacterCodeFinalResponse)  

##### Three Character Country Code Search
@cns.route('/threeCharacterCode/<threeCharacterCode>')
class threeCharacterCode(Resource):
    def get(self, threeCharacterCode):
        threeCharacterCodeInterimResponse = es.search(index="countries", body="{\"query\": {\"match\": {\"alpha3Code\": \"%s\"}}}" % threeCharacterCode)
        threeCharacterCodeFinalResponse = []
        for row in threeCharacterCodeInterimResponse["hits"]["hits"]:
          threeCharacterCodeFinalResponse.append(row["_source"])
        return jsonify(threeCharacterCodeFinalResponse)  


#########################################################################


##### Use elastic query _string search to search city list
@ns.route('/basicsearch')
class basicsearch(Resource):
    @ns.doc(parser=basicCityQuery)
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
        

##### Count of Cities
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

#########################################################################

##### Using Probable Name to determine party type
@pns.route('/partyType')
class partyType(Resource):
    @pns.doc(parser=partyName)
    def post(self):
        args = partyName.parse_args()
        partyNameText = args['partyName']
        resp = pp.tag(partyNameText)
        type = resp[-1]
        if   type in ['Person']:
          return jsonify(partyName=partyNameText,partyTypeConfidence='High',partyType=type)
        elif type in ['Corporation']:
          return jsonify(partyName=partyNameText,partyTypeConfidence='High',partyType=type)
        elif type in ['Household']:
          return jsonify(partyName=partyNameText,partyTypeConfidence='Medium',partyType=type)
        else: 
          return jsonify(partyName=partyNameText,partyTypeConfidence='Low',partyType='Person')

##### Using Probable Name to determine party type
@pns.route('/nameParser')
class partyType(Resource):
    @pns.doc(parser=partyName)
    def post(self):
        args = partyName.parse_args()
        partyNameText = args['partyName']
        resp0 = pp.tag(partyNameText)
        type = resp0[-1]
        finalResponse = dict(resp0[0])
        partyType = {}
        if   type in ['Person']:
          partyType['partyTypeConfidence'] = 'High'
          partyType['partyType'] = type
        elif type in ['Corporation']:
          partyType['partyTypeConfidence'] = 'High'
          partyType['partyType'] = type
        elif type in ['Household']:
          partyType['partyTypeConfidence'] = 'Medium'
          partyType['partyType'] = type
        else:
          partyType['partyTypeConfidence'] = 'Low'
          partyType['partyType'] = 'Person'
        return jsonify(submittedPartyName=partyNameText,parsedParty=finalResponse,partyType=partyType)
 


##### Libpostal Address Parsing 
@ans.route('/')
class addressParser(Resource):
    @ans.doc(parser=addressText)
    def post(self):
        args = addressText.parse_args()
        fullAddressText = args['addressText']
        resp = parse_address(fullAddressText)
        finalResponse = dict((y, x) for x, y in resp)
#        finalResponse = {}
#        for loopera in resp:
#          key = loopera[1] 
#          value = loopera[0] 
#          finalResponse[key] = value
        return jsonify(finalResponse)
 
#########################################################################


if __name__ == '__main__':
#    handler = RotatingFileHandler('/tmp/foo.log', maxBytes=10000, backupCount=1)
#    handler.setLevel(logging.INFO)
#    app.logger.addHandler(handler)
    app.run(debug=False)

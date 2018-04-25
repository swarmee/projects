from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify
import probablepeople as pp
import json
from postal.parser import parse_address


app = Flask(__name__)
api = Api(app,
        version='1.0', 
          title='Swagger Test Page for Name and Address Parsing APIs', 
          description='Name and Address Parsing', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="www.swarmee.net"
         )
app.wsgi_app = ProxyFix(app.wsgi_app)

pns = api.namespace('partyType', description='Simple Party Parser and Typer')

partyName = pns.parser()
partyName.add_argument('partyName', type=str, help='partyName for Processing', location='form')

ans = api.namespace('addressParser', description='Simple Party Type Identification')

addressText = ans.parser()
addressText.add_argument('addressText', type=str, help='The address to be parsed into components', location='form')


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
 


if __name__ == '__main__':
    app.run(debug=False)

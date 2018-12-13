from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, jsonify
import json
import string

countries = []
with open('country-data.json') as json_data:
    d = json.load(json_data)
    for row in d["hits"]["hits"]:
      countries.append(row["_source"]) 

#print(json.dumps(countries , sort_keys = True, indent = 2, ensure_ascii = False))
print('countires loaded')

app = Flask(__name__)
api = Api(app,
        version='1.0', 
          title='Country API', 
          description='Data from from https://restcountries.eu/rest/v2/all', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="www.swarmee.net"
         )
app.wsgi_app = ProxyFix(app.wsgi_app)

ns = api.namespace('country', description='Country Namespace')

##### Two Character Country Code Search
@ns.route('/twoCharacterCode/<twoCharacterCode>')
class twoCharacterCode(Resource):
    def get(self, twoCharacterCode):
        responseContent = {}
        twoCharacterCode = twoCharacterCode.upper()
        for country in countries:
          if country["alpha2Code"] == twoCharacterCode:
            responseContent = country
        try:
          responseContent 
        except NameError:
          responseContent = {'error' : 'not found'}
        return responseContent

if __name__ == '__main__':
    app.run(debug=False)

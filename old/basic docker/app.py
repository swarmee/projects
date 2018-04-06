from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, 
          version='1.0', 
          title='Get Country Details', 
          description='A simple Country Details API', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="www.swarmee.net"
          )

ns = api.namespace('country', 
                   description='Country API operations')

country = api.model('country', 
          {'id'         : fields.Integer(readOnly=True, description='The country unique identifier'),
           'countryCode': fields.String (readOnly=True, description='Country Code'),
           'countryName': fields.String (required=True, description='The country name'),
           'countryLat' : fields.String (required=False, description='The country geo lat'),
           'countryLong': fields.String (required=False, description='The country geo long'),           
                        }
                 )

class countryDAO(object):
    def __init__(self):
        self.counter = 0
        self.countries = []

    def get(self, id):
        for country in self.countries:
            if country['id'] == id:
                return country
        api.abort(404, "Country {} doesn't exist".format(id))

    def get(self, countryCode):
        for country in self.countries:
            if country['countryCode'] == countryCode:
                return country
        api.abort(404, "Country {} doesn't exist".format(countryCode))

    def create(self, data):
        country = data
        country['id'] = self.counter = self.counter + 1
        self.countries.append(country)
        return country

DAO = countryDAO()
DAO.create({'countryLat' : '-26.447531','countryLong' : '135.374044', 'countryName': 'AUSTRALIA'	   , 'countryCode': 'AU'})
DAO.create({'countryLat' : '-26.447531','countryLong' : '135.374044', 'countryName': 'THAILAND'      , 'countryCode': 'TH'})
DAO.create({'countryLat' : '-26.447531','countryLong' : '135.374044', 'countryName': 'CHINA'         , 'countryCode': 'CN'})
DAO.create({'countryLat' : '-26.447531','countryLong' : '135.374044', 'countryName': 'NEW ZEALAND'   , 'countryCode': 'NZ'})
DAO.create({'countryLat' : '-26.447531','countryLong' : '135.374044', 'countryName': 'FRANCE'        , 'countryCode': 'FR'})
DAO.create({'countryLat' : '-26.447531','countryLong' : '135.374044', 'countryName': 'JAPAN'         , 'countryCode': 'JP'})
DAO.create({'countryLat' : '-26.447531','countryLong' : '135.374044', 'countryName': 'UNITED STATES' , 'countryCode': 'US'})
DAO.create({'countryLat' : '-26.447531','countryLong' : '135.374044', 'countryName': 'RUSSIA'        , 'countryCode': 'RU'})


@ns.route('/')
class countryList(Resource):
    '''Shows a list of all countries'''

    @ns.marshal_list_with(country)
    def get(self):
        '''List all countries'''
        return DAO.countries

@ns.route('/<int:id>')
@ns.response(404, 'Country not found')
@ns.param('id', 'The country id')
class Country(Resource):
    '''Show a single country based on record id'''
    @ns.marshal_with(country)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

@ns.route('/<string:countryCode>')
@ns.response(404, 'Country not found')
@ns.param('countryCode', 'The country identifier')
class Country(Resource):
    '''Show a single country based on countryCode'''
    @ns.marshal_with(country)
    def get(self, countryCode):
        '''Fetch a given resource'''
        return DAO.get(countryCode)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

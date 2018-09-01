from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, jsonify
import requests
import urllib3
urllib3.disable_warnings()

app = Flask(__name__)
api = Api(app,
	      version='1.0', 
          title='partySearch', 
          description='Simple partySearch Example Api', 
          prefix="/v1",
          contact="john@swarmee.net",
          contact_url="http://www.swarmee.net"
         )
app.wsgi_app = ProxyFix(app.wsgi_app)

ns = api.namespace('search', description='Simple partySearch Api')
nameSearchPost = ns.parser()
nameSearchPost.add_argument('nameSearchTerm', type=str, help='name search terms', location='form')
addressSearchPost = ns.parser()
addressSearchPost.add_argument('addressSearchTerm', type=str, help='address search terms', location='form')


namePayload = api.model('namePayload', {'nameSearchPostPayLoad': fields.String(default='James', required=True, description='name Search Text')})


host = 'elasticsearch'
requestHeaders = {'user-agent': 'my-python-app/0.0.1', 
                  'content-type': 'application/json'}

requestURL = 'http://%s:9200/real-estate-sales/_search' % (host)

def populateNameSearch(nameSearchTerm):
    return {
  "query": {
    "nested": {
      "path": "role.party.name",
      "query": {
        "match": {
          "role.party.name.fullName":  { "query" : nameSearchTerm, "operator" : "AND"  }
        }
      }
    }
  },
  "aggs": {
    "partyNesting": {
      "nested": {
        "path": "role.party"
      },
      "aggs": {
        "partyFilter": {
          "filter": {
            "nested": {
              "path": "role.party.name",
              "query": {
                "match": {
                  "role.party.name.fullName": { "query" : nameSearchTerm, "operator" : "AND"  }
                }
              }
            }
          },
          "aggs": {
            "nameNesting": {
              "nested": {
                "path": "role.party.name"
              },
              "aggs": {
                "nameDetails": {
                  "terms": {
                    "field": "role.party.name.fullName.keyword",
                    "size": 10
                  }
                }
              }
            },
            "addressNesting": {
              "nested": {
                "path": "role.party.address"
              },
              "aggs": {
                "nameDetails": {
                  "terms": {
                    "field": "role.party.address.streetAddress.keyword",
                    "size": 10
                  }
                }
              }
            },
            "accountNesting": {
              "nested": {
                "path": "role.party.account"
              },
              "aggs": {
                "nameDetails": {
                  "terms": {
                    "field": "role.party.account.number",
                    "size": 10
                  }
                }
              }
            },
            "identificationNesting": {
              "nested": {
                "path": "role.party.identification"
              },
              "aggs": {
                "nameDetails": {
                  "terms": {
                    "field": "role.party.identification.identifier.keyword",
                    "size": 50
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "size": 0
}

def populateAddressSearch(addressSearchTerm):
    return {
  "query": {
    "nested": {
      "path": "role.party.address",
      "query": {
        "match": {
          "role.party.address.streetAddress":  { "query" : addressSearchTerm, "operator" : "AND"  }
        }
      }
    }
  },
  "aggs": {
    "partyNesting": {
      "nested": {
        "path": "role.party"
      },
      "aggs": {
        "partyFilter": {
          "filter": {
            "nested": {
              "path": "role.party.address",
              "query": {
                "match": {
                  "role.party.address.streetAddress": { "query" : addressSearchTerm, "operator" : "AND"  }
                }
              }
            }
          },
          "aggs": {
            "nameNesting": {
              "nested": {
                "path": "role.party.name"
              },
              "aggs": {
                "nameDetails": {
                  "terms": {
                    "field": "role.party.name.fullName.keyword",
                    "size": 10
                  }
                }
              }
            },
            "addressNesting": {
              "nested": {
                "path": "role.party.address"
              },
              "aggs": {
                "nameDetails": {
                  "terms": {
                    "field": "role.party.address.streetAddress.keyword",
                    "size": 10
                  }
                }
              }
            },
            "accountNesting": {
              "nested": {
                "path": "role.party.account"
              },
              "aggs": {
                "nameDetails": {
                  "terms": {
                    "field": "role.party.account.number",
                    "size": 10
                  }
                }
              }
            },
            "identificationNesting": {
              "nested": {
                "path": "role.party.identification"
              },
              "aggs": {
                "nameDetails": {
                  "terms": {
                    "field": "role.party.identification.identifier.keyword",
                    "size": 50
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "size": 0
}
###################################################################################################
@ns.route('/search/NamePayload')
class documentNameSearchPostPayload(Resource):
    @ns.expect(namePayload)
    def post(self):
        nameSearchTerm = api.payload['nameSearchPostPayLoad']
        requestBody = populateNameSearch(nameSearchTerm)
        r = requests.post(requestURL,
                         auth=('test','test'),
                         json=requestBody,
                         headers=requestHeaders,
                         verify=False)
        r = r.json()
        return r 


@ns.route('/search/name')
class documentNameSearchPost(Resource):
    @ns.doc(parser=nameSearchPost)
    def post(self):
        args = nameSearchPost.parse_args()
        nameSearchTerm = args['nameSearchTerm']
        requestBody = populateNameSearch(nameSearchTerm)
        r = requests.post(requestURL,
                         auth=('test','test'),
                         json=requestBody,
                         headers=requestHeaders,
                         verify=False)
        r = r.json()
        return r 


@ns.route('/search/address')
class documentAddressSearchPost(Resource):
    @ns.doc(parser=addressSearchPost)
    def post(self):
        args = addressSearchPost.parse_args()
        addressSearchTerm = args['addressSearchTerm']
        requestBody = populateAddressSearch(addressSearchTerm)
        r = requests.post(requestURL,
                         auth=('test','test'),
                         json=requestBody,
                         headers=requestHeaders,
                         verify=False)
        r = r.json()
        return r         

@ns.route('/search/name/<nameSearchTerm>')
class documentNameSearch(Resource):
    def get(self, nameSearchTerm):
        requestBody = populateNameSearch(nameSearchTerm)
        r = requests.post(requestURL,
                         auth=('test','test'),
                         json=requestBody,
                         headers=requestHeaders,
                         verify=False)
        r = r.json()
        return r       

@ns.route('/search/address/<addressSearchTerm>')
class documentAddressSearch(Resource):
    def get(self, addressSearchTerm):
        requestBody = populateAddressSearch(addressSearchTerm)
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






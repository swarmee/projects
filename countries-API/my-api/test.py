import json
countries = []
with open('country-data.json') as json_data:
    d = json.load(json_data)
    for row in d["hits"]["hits"]:
      countries.append(row["_source"]) 

print(json.dumps(countries , sort_keys = True, indent = 2, ensure_ascii = False))

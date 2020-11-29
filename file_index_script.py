import json
import requests
from requests.auth import HTTPBasicAuth

with open('schema_health.json') as json_file:
    goverment = json.load(json_file)

headers = {
  'Content-Type': 'application/json;',
    'Authorization': 'ApiKey M2N0ZUVuWUJ2c1hhU3JQWjZXRnA6cFFUUjZGcUNRQ2liYzRFWnp3S0RUdw==',
}


url = 'https://63b59e3d9c4a4128ade4896a2e5f9811.us-central1.gcp.cloud.es.io:9243/test_index/_doc/'
# conn = http.client.HTTPSConnection("localhost", 9200)
for key in goverment:
    req_url = goverment[key]['identifier']
    print(json.dumps(goverment[key]))
    r = requests.put(url+req_url, data=(json.dumps(goverment[key])).encode('utf-8'), headers=headers, auth=HTTPBasicAuth('elastic', 'jUU9t4jN7I8HbGIa7wudWB7F'))
    print(r.content)
    # break




print(req_url)

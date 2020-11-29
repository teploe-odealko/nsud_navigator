import json
import requests
# import http.client

with open('goverment.json') as json_file:
    # contents = json_file.read()
    # goverment = ast.literal_eval(contents)
    goverment = json.load(json_file)

headers = {
  'Content-Type': 'application/json; charset=utf-8',

}
url = 'http://localhost:9200/test_index/_doc/'
# conn = http.client.HTTPSConnection("localhost", 9200)
for key in goverment:
    # print(goverment[key])
    req_url = goverment[key]['identifier']

    # print(req_url)
    # conn.request("PUT", "/test_index/_doc/" + req_url, str(goverment[key]).encode('utf-8'), headers)
    # res = conn.getresponse()
    # data = res.read()
    # print(data.decode("utf-8"))
    # str_put = str_put.replace('"', '$')
    # str_put = str_put.replace("'", '"')
    # str_put = str_put.replace("$", "'")
    # print(str_put)
    r = requests.put(url+req_url, data=(json.dumps(goverment[key])).encode('utf-8'), headers=headers)
    print(r.content)
    # break




print(req_url)

import requests
from requests.auth import HTTPBasicAuth
import json
import simplejson
import sys
import glob

result = []

#with open(sys.argv[1]) as data_file:
#	json_rule = json.dumps(json.load(data_file))
with open('ruletable_4.json') as data_file:
	json_rule = json.dumps(json.load(data_file))

#json_rule = json.dumps(result)

headers = {'Content-Type':'application/json' , 'Accept':'application/json'}
response = requests.post('http://160.39.252.121:8181/onos/v1/flows/of%3A0000687f7429badf', data=json_rule, auth=('onos', 'rocks'), headers=headers)
print response.status_code

with open('ruletable_5.json') as data_file:
	json_rule = json.dumps(json.load(data_file))

#json_rule = json.dumps(result)

headers = {'Content-Type':'application/json' , 'Accept':'application/json'}
response = requests.post('http://160.39.252.121:8181/onos/v1/flows/of%3A0000687f7429badf', data=json_rule, auth=('onos', 'rocks'), headers=headers)
print response.status_code

with open('ruletable_6.json') as data_file:
	json_rule = json.dumps(json.load(data_file))

#json_rule = json.dumps(result)

headers = {'Content-Type':'application/json' , 'Accept':'application/json'}
response = requests.post('http://160.39.252.121:8181/onos/v1/flows/of%3A0000687f7429badf', data=json_rule, auth=('onos', 'rocks'), headers=headers)
print response.status_code

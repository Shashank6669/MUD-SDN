import requests
from requests.auth import HTTPBasicAuth
import json
import sys

device_id = 'of:5e3e486e73020629' #pica8
base_url = 'http://160.39.139.142:8181/onos/v1'

#headers = {'Content-Type':'application/json' , 'Accept':'application/json'}
# Fetch the flows id's 
response = requests.get('http://160.39.139.142:8181/onos/v1/flows/of%3A0000687f7429badf', auth=('onos', 'rocks'))
rules = response.json()
flows_ids = []
for flow in rules['flows']:
	flows_ids.append(flow['id'])

for flow_id in flows_ids:
	print flow_id
	response = requests.delete('http://160.39.139.142:8181/onos/v1/flows/of%3A0000687f7429badf', auth=('onos', 'rocks'))
	print response.status_code


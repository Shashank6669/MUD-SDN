#!/usr/bin/python
import requests
import json
import argparse
from requests.auth import HTTPBasicAuth
import flowtable

def ACL(IP,ID):
	reqURL = "http://"+IP+":8181/onos/v1/flows"
	reqURL_dev = reqURL+ID
	print(reqURL)
	print(reqURL_dev)
	
	fid, flow, rcode = GET(reqURL)
	
	print(fid)
	print(rcode)
	print(flows)

	"""flowid = 18577352444689406
	rcode = DEL(reqURL_dev,flowid)
    """ 

    mac = 
	

def GET(URL):
	response = requests.get(URL, auth=('onos', 'rocks'))
	print response.status_code
	flow_resp = response.json()
	flow_ids = []
	for flow in flow_resp['flows']:
		#print('hello')
		flow_ids.append(flow['id'])
	
	return flow_ids, flow_resp, response.status_code
	

def POST(URL, flow_json):

	json_rule = flow_json
	headers = {'Content-Type':'application/json' , 'Accept':'application/json'}
	response = requests.post(URL, data=json_rule, auth=('onos', 'rocks'), headers=headers)
	print response.status_code

	return response.status_code

def DEL(URL, flowid):

	url_del = URL+"/"+str(flowid)
	print(url_del)
	#headers = {'Content-Type':'application/json' ,'Accept: application/json'}
	response = requests.delete(url_del, auth=('onos', 'rocks'))
	#print response.status_code
	return response.status_code

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("ControllerIP",help="Specify Controller IP")

	args = parser.parse_args()
	#devID = "/of%3A0000687f7429badf"
	devID = "/of%3A0000000000000001"
	ACL(args.ControllerIP,devID)
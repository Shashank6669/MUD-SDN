import requests
import json
import argparse
#import flowtable

from requests.auth import HTTPBasicAuth
from pprint import pprint

c = 0

def ACL_Blacklist(IP,ID,mac):
	global c
	reqURL = "http://"+IP+":8181/onos/v1/flows"
	reqURL_dev = reqURL+ID
	print(reqURL)
	print(reqURL_dev)
	
	fid, flow, rcode = GET(reqURL)
	
	#print(fid)
	#print(rcode)

	#pprint(flow['flows'][2])
	#pprint(flow)


	#x = flow['flows'][2]['selector']['criteria'][1]['mac']    -----destination mac
	#y = flow['flows'][2]['selector']['criteria'][2]['mac']    -----Source mac
	delete_id = []
	if (c == 0):

		for i in flow['flows']:
			if(len(i['selector']['criteria']) == 3):
				#print(i['selector']['criteria'])
				
				fmac_dst = i['selector']['criteria'][1]['mac'].encode('ascii', 'ignore')
				fmac_src = i['selector']['criteria'][2]['mac'].encode('ascii', 'ignore')
				

				if(fmac_dst.lower() == mac.lower() or fmac_src.lower() == mac.lower()):
					delete_id.append(i['id'])
					
			
				
			#print(i['selector']['criteria'])
		
		pprint(delete_id)
	
		for d in delete_id:
			response = DEL(reqURL_dev, d)
			print(response)

		c++
	


def GET(URL):
	response = requests.get(URL, auth=('onos', 'rocks'))
	print response.status_code
	flow_resp = response.json()
	flow_ids = []
	for flow in flow_resp['flows']:
		#print('hello')
		flow_ids.append(flow['id'])

	return flow_ids, flow_resp, response.status_code
	

def POST(URL, flow):
	json_rule = json.dumps(flow)
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
	devID = "/of%3A0000687f7429badf"
	
	#devID = "/of%3A0000000000000001"
	count = 0
	mac = "00:1F:3B:05:2A:C9"
	ACL_Blacklist(args.ControllerIP,devID,mac, count)


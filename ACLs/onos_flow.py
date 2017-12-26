import requests
import json
import argparse
import socket


from flowtable import *
from quarantine_flow import *
#from static_flow import *
from requests.auth import HTTPBasicAuth
from pprint import pprint

c = 0


def ACL_Blacklist(IP,ID,mac,ip1,ip2):
	global c
	reqURL = "http://"+IP+":8181/onos/v1/flows/"
	reqURL_dev = reqURL+ID
	
	print(reqURL)
	print(reqURL_dev)
	
	#fid, flow, rcode = GET(reqURL)
	
	#print(fid)
	#print(rcode)

	#pprint(flow['flows'][2])
	#pprint(flow)


	#x = flow['flows'][2]['selector']['criteria'][1]['mac']    -----destination mac
	#y = flow['flows'][2]['selector']['criteria'][2]['mac']    -----Source mac
	
	if (c == 0):
		CLEAR(reqURL,reqURL_dev)


	"""
	delete_id = []
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
	"""

	for f in range(3):
		flow = create_flow(mac, ip1, ip2, f)
    	post_response= str(POST(reqURL_dev, flow))
        print(post_response) 
	
	c = c + 1
"""
def static_profile(IP,ID,mac,ip1):
	##stop onos-app-fwd in ONOS CLI
	reqURL = "http://"+IP+":8181/onos/v1/flows/"
	reqURL_dev = reqURL+ID
	print(reqURL)
	print(reqURL_dev)
	
	fid, flow, rcode = GET(reqURL)

	device = devices.find_one({'mac_address': mac})
	acl = device['static_profile']

	dns_name = acl[0]['in']['dnsname']
	ip2 = socket.gethostbyname(acl[0]['in']['dnsname'])

	delete_id = []

	# Delete all existing flows for the device
		for i in flow['flows']:
			if(len(i['selector']['criteria']) == 3):    
				#print(i['selector']['criteria'])
				
				fmac_dst = i['selector']['criteria'][1]['mac'].encode('ascii', 'ignore')
				fmac_src = i['selector']['criteria'][2]['mac'].encode('ascii', 'ignore')

				if(fmac_dst.lower() == mac.lower() or fmac_src.lower() == mac.lower()):
					delete_id.append(i['id'])
					
			#print(i['selector']['criteria'])
		
		#pprint(delete_id)

		for d in delete_id:
			response = DEL(reqURL_dev, d)
			print(response)
	
	#Add flows according to MUD profile.
	for f in range(3):
		flow = S_flow(mac,ip1,ip2,f)
		post_response=str(POST())

"""

def QUARANTINE(IP,ID,mac):
	global c
	reqURL = "http://"+IP+":8181/onos/v1/flows/"
	reqURL_dev = reqURL+ID

	if(c == 0):
		CLEAR(reqURL,reqURL_dev)

	for f in range(2):
		flow = Q_flow(mac, f)
    	post_response = POST(reqURL_dev, flow)
        print("Flow rule add response: "+str(f)+" "+str(post_response)) 

        c = c + 1


def CLEAR(reqURL,reqURL_dev):

	fid, flow, rcode = GET(reqURL)

	delete_id = []
	for i in flow['flows']:
			if(len(i['selector']['criteria']) == 3):
				delete_id.append(i['id'])

	for d in delete_id:
			response = str(DEL(reqURL_dev, d))
			print("Delete response  "+str(d)+"  :  "+response)


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


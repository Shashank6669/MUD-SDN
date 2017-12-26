import requests
import json
import argparse
import socket


from flowtable import *
from quarantine_flow import *
#from static_flow import *
from requests.auth import HTTPBasicAuth
from pprint import pprint

def POST(URL, flow):
        json_rule = json.dumps(flow)
        headers = {'Content-Type':'application/json' , 'Accept':'application/json'}
        response = requests.post(URL, data=json_rule, auth=('onos', 'rocks'), headers=headers)
        print response.status_code
        return response.status_code


IP = '160.39.253.131'
ID = '/of%3A0000687f7429badf'
mac = '74:E5:43:1D:A5:33'

reqURL = "http://"+IP+":8181/onos/v1/flows/"
reqURL_dev = reqURL+ID

for f in range(2):
	flow = Q_flow(mac, f)
	post_response= str(POST(reqURL_dev, flow))
	print("Flow rule add response: "+str(f)+" "+post_response) 



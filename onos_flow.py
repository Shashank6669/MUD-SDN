#!/usr/bin/python
import requests
import json
import argparse
from requests.auth import HTTPBasicAuth


def ACL(IP,ID):
	reqURL = "http://"+IP+":8181/onos/v1/flows"
	reqURL_dev = reqURL+ID
	print(reqURL)
	print(reqURL_dev)
	
	flows = GET(reqURL)
	print(flows)

def GET(URL):
	response = requests.get(URL, auth=('onos', 'rocks'))
	flows = response.json()
	return flows
#def POST():

#def DEL():





if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("ControllerIP",help="Specify Controller IP")

	args = parser.parse_args()
	devID = "/of%3A0000687f7429badf"
	ACL(args.ControllerIP,devID)
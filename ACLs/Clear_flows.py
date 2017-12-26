from ONOS_API import CLEAR
from ONOS_API import GET
import requests
import argparse


devID = "of%3A0000687f7429badf"
parser = argparse.ArgumentParser()
parser.add_argument("ControllerIP",help="Specify Controller IP")
args = parser.parse_args()

print(args.ControllerIP)

reqURL = "http://"+args.ControllerIP+":8181/onos/v1/flows/"
reqURL_dev = reqURL+devID

print(reqURL)
print(reqURL_dev)

CLEAR(reqURL,reqURL_dev)


#from mongo_ops import *
import json
import urllib2

#Allow access to certain websites for a device
ACL = {        
      "priority": 10,
      "timeout": 0,
      "isPermanent": True,
      "deviceId": "of:0000687f7429badf",
      "treatment": {
        "instructions": [
          {
            "type": "OUTPUT",
            "port": "1"
          }
        ]
      },
      "selector": {
        "criteria": [
          {
            "type": "IN_PORT",
            "port": 6
          },
          {
            "type": "ETH_SRC",
            "mac": "00:1F:3B:05:2A:C9"
          },
          {
            "type": "ETH_DST",
            "mac": "60:E3:27:9B:44:BF"
          }
        ]
      }
    }
url = 'http://160.39.139.142:8181/onos/v1/flows/of%3A0000687f7429badf'
username = 'onos'
password = 'rocks'
p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

req = urllib2.Request('http://160.39.139.142:8181/onos/v1/flows/of%3A0000687f7429badf')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(ACL, indent=4, sort_keys=False))
print response

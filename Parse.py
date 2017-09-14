#!/usr/bin/python

"""
This code parses the MUD JSON file and extracts the ACL.
"""
import json
import socket

def ACL():
 
     "Parse the JSON MUD file to extract Match rules"

     with open('/usr/local/etc/controller/lighting-example.json') as data_file:
      d = json.load(data_file)

     #print(d)

     acl = d["ietf-access-control-list:access-lists"]["acl"]
     #print(acl)


#inbound rules#################################################################
     idirection  = str(acl[0]["acl-name"])
     #print(idirection)

     iace = acl[0]["access-list-entries"]["ace"][0]
     #print(iace)

     #input action
     iact = str(iace["actions"]["permit"]) 
     print(iact)
     if iact == '[None]':
      iact = 'ACCEPT'
     print(iact)

     # Matching rules
     imatch  = iace["matches"]
     #print(imatch)

     #inbound port
     iport = str(imatch["destination-port-range"]["lower-port"])
     #print(iport)

     #Source IP
     sip = imatch["ietf-acl-dnsname:source-hostname"]
     #print(sip)

     host = sip.split("//",1)[1]
     host = host.split("/", 1)[0]
     #print(host)
     TranslatedIp = socket.gethostbyname(host)
     #print(TranslatedIp)



     #protocol
     iproto = str(imatch["protocol"])
     #print(iproto)
################################################################################
     #print("Direction: "+ idirection)
     #print("Drop Action: " + act)
     #print("Port: " + iport)
     #print("Source IP: " + TranslatedIp)
     #print("Protocol:" + iproto)

#outbound rules#################################################################
     odirection  = str(acl[1]["acl-name"])
     #print(odirection)

     oace = acl[1]["access-list-entries"]["ace"][0]
     #print(oace)

     #action
     oact = str(iace["actions"]["permit"]) 
     #print(oact)
     if oact == '[None]':
      oact = 'ACCEPT'
     #print(oact)

     # Matching rules
     omatch  = oace["matches"]
     #print(omatch)

     #outbound port
     oport = str(omatch["source-port-range"]["lower-port"])
     #print(oport)

     #Destination IP
     dip = omatch["ietf-acl-dnsname:destination-hostname"]
     #print(dip)

     host = dip.split("//",1)[1]
     host = host.split("/", 1)[0]
     #print(host)
     TranslatedIp = str(socket.gethostbyname(host))
     #print(TranslatedIp)

     #protocol
     oproto = str(omatch["protocol"])
     #print(oproto)
#################################################################################
     #print("------------------------------------------------------------------------")
     #print("Direction: "+ odirection)
     #print("Drop Action: " + act)
     #print("Port: " + oport)
     #print("Destination IP: " + str(TranslatedIp))
     #print("Protocol:" + oproto) 

     #return (TranslatedIp,iport,act,iproto) 
     inbound = []
     inbound.append(TranslatedIp)
     inbound.append(iport)
     inbound.append(iact)
     inbound.append(iproto)
     #print(inbound)
     outbound = []
     outbound.append(TranslatedIp)
     outbound.append(oport)
     outbound.append(oact)
     outbound.append(oproto)
     #print(outbound)
     return inbound,outbound
     
if __name__ == '__main__':
    setLogLevel( 'info' )
    ACL()

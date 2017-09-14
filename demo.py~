#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import time
import json
import os
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
     
     

def MudNet():
    

    "Create an empty network and add nodes to it."

    net = Mininet( controller=Controller )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding MUD Architecture Blocks\n' )
    hrs = net.addHost( 'RadServer', ip='10.0.0.1' )
    hms = net.addHost( 'MUDServer', ip='10.0.0.2' )
    hrc = net.addHost( 'RadClient', ip='10.0.0.3' )

    info( '*** Adding switch\n' )
    s3 = net.addSwitch( 's3' )
    

    info( '*** Creating links\n' )
    net.addLink( hrs, s3 )
    net.addLink( hms, s3 )
    net.addLink( hrc, s3 )

    info( '*** Starting network\n')
    net.start()

    hrs.cmdPrint('sudo radiusd -X > radbug.txt 2>&1 &')
    hrs.cmd('sleep 15')
    hms.cmdPrint('python -m SimpleHTTPServer 80 &')
    hms.cmd('sleep 5')
    hrc.cmdPrint('sudo echo "User-Name=Shashank, User-Password=IOTSECURITY, Columbia-MUD-URI=http://10.0.0.2/mud/lighting-example.json" | /usr/local/bin/radclient -x 10.0.0.1 auth testing123')
    #s3.cmdPrint('ifconfig')
    net.stop()
    os.system("sleep 2")


################################################################################
def emptynet():
    
    "Create a mininet SDN with custom flow tables."
    #host,port,action,protocol = ACL()
    x,y = ACL()
    print('Inbound access entry: '+str(x))
    print('////////////////////////')
    print('Outbound access entry: '+str(y))
    
    net = Mininet( controller= Controller )
    info( '*** Adding controller\n' )
    #net.addController( 'c0' )                # Disable controller to create flows manually
    

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='192.168.0.1', mac = '00:00:00:00:00:01' )  #Desktop connected to home network
    h2 = net.addHost( 'h2', ip='192.168.0.2', mac = '00:00:00:00:00:02' )  #IoT Device LED Light connected to home network
    h3 = net.addHost( 'h3', ip=x[0], mac ='00:00:00:00:00:03' ) ####### IP address allowed for communication
     
    info( '*** Adding switch\n' )
    s4 = net.addSwitch( 's4' )

    info( '*** Creating links\n' )
    net.addLink( h1, s4 )
    net.addLink( h2, s4 )
    net.addLink( h3, s4 ) 

    info( '*** Starting network\n')
    net.start()
    
    
    h3.cmdPrint('route add default gw 128.59.105.254 h3-eth0')
    h3.cmdPrint('arp -s 128.59.105.254 00:00:00:00:33:33')

    h1.cmdPrint('route add default gw 192.168.0.254 h1-eth0')
    h1.cmdPrint('arp -s 192.168.0.254 00:00:00:00:00:11:11')    

    h2.cmdPrint('route add default gw 192.168.0.254 h2-eth0')
    h2.cmdPrint('arp -s 192.168.0.254 00:00:00:00:00:11:11')

    h3.cmdPrint('sudo python -m SimpleHTTPServer 80 &')

    #os.system("more tables.txt")
    os.system("ovs-ofctl add-flows s4 tables.txt")
    
    
    info( '*** Running CLI\n' )
    CLI( net )
    
    info( '*** Stoping network' )
    net.stop()
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    
    MudNet()
    emptynet()
    
    

#!/usr/bin/python

'This example shows how to work with Radius Server and implement flow tables based ACL with two APS and a host.'

#      c0
#      |
#      s4------AP1-----IoT
#      / \
#     /   \
#    h1    AP2
#           \
#         cloud server

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP, OVSSwitch, OVSAP, UserAP
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import os
import Parse

################################################################################
def emptynet():
    
    "Create a mininet SDN with custom flow tables."
    #host,port,action,protocol = ACL()
    x,y = Parse.ACL()
    print('Inbound access entry: '+str(x))
    print('////////////////////////')
    print('Outbound access entry: '+str(y))
    
    net = Mininet(  controller=Controller, link=TCLink, accessPoint=OVSAP, switch=OVSSwitch, enable_wmediumd=True, enable_interference=False )
    print( '*** Adding controller\n' )
    c0 = net.addController( 'c0', controller=Controller, ip='127.0.0.1', port=6633 )                # Disable controller to create flows manually

    print( '*** Adding Nodes\n' )
    h1 = net.addHost( 'h1', ip='192.168.0.1', mac = '00:00:00:00:00:01', position='130,140,0' )  #Desktop connected to home network
    sta2 = net.addStation( 'sta2', ip='192.168.0.2', mac = '00:00:00:00:00:02', position='150,140,0' )  #IoT Device LED Light connected to home network
    sta3 = net.addStation( 'sta3', ip=x[0], mac ='00:00:00:00:00:03', position='170,140,0' ) ####### IP address allowed for communication
     
    print( '*** Adding accesspoints\n' )
    #ap1 = net.addAccessPoint( 'ap1', ssid='simplewifi1', mode='a', channel='36', position='140,120,0' )
    ap2 = net.addAccessPoint( 'ap2', ssid='simplewifi1', mode='a', channel='36', position='150,100,0' )
    ap3 = net.addAccessPoint( 'ap3', ssid='simplewifi1', mode='a', channel='36', position='160,120,0' )

    print("*** Adding switch\n")
    s4 = net.addSwitch( 's4', position='150,120,0' )

    print "*** Configuring Propagation Model"
    net.propagationModel("logDistancePropagationLossModel", exp=3.5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()    


    print( '*** Creating links\n' )
    net.addLink( s4, h1 )
    net.addLink( s4, ap2 )
    net.addLink( s4, ap3 )
    net.addLink( sta2, ap2 )
    net.addLink( sta3, ap3 ) 
    
    print( '*** Starting network\n')
    net.build()
    c0.start()
    #ap1.start( [c0] )
    ap2.start( [c0] )
    ap3.start( [c0] )
    s4.start( [c0] )
    
    
    sta3.cmdPrint('route add default gw 128.59.105.254 sta3-wlan0')
    sta3.cmdPrint('arp -s 128.59.105.254 00:00:00:00:33:33')

    h1.cmdPrint('route add default gw 192.168.0.254 h1-eth0')
    h1.cmdPrint('arp -s 192.168.0.254 00:00:00:00:00:11:11')    

    sta2.cmdPrint('route add default gw 192.168.0.254 sta2-wlan0')
    sta2.cmdPrint('arp -s 192.168.0.254 00:00:00:00:00:11:11')

    sta3.cmdPrint('sudo python -m SimpleHTTPServer 80 &')

    os.system("more tables.txt")
    os.system("ovs-ofctl add-flows s4 tables.txt")
    
    print "*** Building graph"
    net.plotGraph(max_x=300, max_y=300)
    

    print( '*** Running CLI\n' )
    CLI( net )
    
    print( '*** Stoping network' )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    #topology()
    emptynet()

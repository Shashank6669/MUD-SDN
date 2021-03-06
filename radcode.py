#!/usr/bin/python

'This example shows how to work with Radius Server'

from mininet.net import Mininet
from mininet.node import  Controller, UserAP, OVSKernelAP, OVSAP
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import os

def topology():
    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, accessPoint=UserAP, enable_wmediumd=True, enable_interference=False )

    print "*** Creating nodes"
    sta1 = net.addStation( 'sta1', radius_passwd='sdnteam', encrypt='wpa2', radius_identity='joe', position='110,80,0', ip='10.0.0.1' )
  
    sta2 = net.addStation( 'sta2', radius_passwd='hello', encrypt='wpa2', radius_identity='bob', position='190,80,0', ip='10.0.0.2' )
    
    ap1 = net.addAccessPoint( 'ap1', ssid='simplewifi1', authmode='8021x', mode='a', channel='36', encrypt='wpa2', position='150,100,0' )

    ap2 = net.addAccessPoint( 'ap2', ssid='simplewifi1', mode='a', channel='36', position='150,120,0' )

    c0 = net.addController('c0', controller=Controller, ip='127.0.0.1', port=6633 )
 
    #h3 = net.addHost('h3', ip='10.0.0.3', position='150,120,0')
    #s3 = net.addSwitch('s3', position='150,110,0')
    
    sta3 = net.addStation('sta3', position='150,140,0', ip='10.0.0.3')
    print "*** Configuring Propagation Model"
    net.propagationModel("logDistancePropagationLossModel", exp=3.5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()
    
    print "*** Associating Stations"
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)
    net.addLink(ap1, ap2)
    net.addLink(sta3, ap2)
     #######
   
    
     #net.addLink(h3,s3)    

    print "*** Starting network"
    net.build()
    c0.start()
    ap1.start( [c0] )
    ap2.start([c0])
    print "*** Building graph"
    net.plotGraph(max_x=300, max_y=300)

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

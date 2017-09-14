#!/usr/bin/python

'This example shows how to work with Radius Server'

from mininet.net import Mininet
from mininet.node import  Controller, UserAP
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, accessPoint=UserAP, enable_wmediumd=True, enable_interference=True )
    
    print "*** Creating Controller"
    c0 = net.addController('c0', controller=Controller, ip='127.0.0.1', port=6633 )

    print "*** Creating AP"
    ap1 = net.addAccessPoint( 'ap1', ssid='simplewifi', authmode='8021x', mode='a', channel='36', encrypt='wpa2', position='150,100,0', radius_server='192.168.0.4', shared_secret='testing123' )

    print "*** Creating nodes"
    sta1 = net.addStation( 'sta1', radius_passwd='IOTSECURITY', encrypt='wpa2', radius_identity='Shashank', position='110,120,0', ip='192.168.0.4', mac='00:00:00:00:00:14' )
    sta2 = net.addStation( 'sta2', radius_passwd='IOTSECURITY', encrypt='wpa2', radius_identity='Shashank', position='200,100,0',ip='192.168.0.5', mac='00:00:00:00:00:15' )
        
    
    #h1 = net.addHost('h1', ip='192.168.0.1', mac='00:00:00:00:00:11')
    #h2 = net.addHost('h2', ip='192.168.0.2', mac='00:00:00:00:00:12')
    #h3 = net.addHost('h3', ip='192.168.0.3', mac='00:00:00:00:00:13')
    
    #net.addLink( h1, ap1 )
    #net.addLink( h2, ap1 )
    #net.addLink( h3, ap1 )
    
    #s1 = net.addSwitch('s1')
   
    #net.addLink( h1, s1 )
    #net.addLink( h2, s1 )
    #net.addLink( h3, s1 )
     
    #print "*** Linking switch and AP"
    #net.addLink( s1, ap1)

    print "*** Configuring Propagation Model"
    net.propagationModel("logDistancePropagationLossModel", exp=3.5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating Stations"
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    print "*** Starting network"
    net.build()
    c0.start()
    
    ap1.start( [c0] )
    sta1.cmdPrint('sudo radiusd -X > radbug.txt 2>&1 &')
    #h1.cmdPrint('sudo radiusd -X > radbug.txt 2>&1 &')
    #h1.cmdPrint('sleep 15')
    #print "*** Building graph"
    #net.plotGraph(max_x=300, max_y=300)

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

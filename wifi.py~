#!/usr/bin/python

'This example creates a simple network topology with 1 AP and 2 stations'

from mininet.net import Mininet
from mininet.node import  Controller, OVSKernelAP, UserAP, OVSAP, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSAP, switch=OVSSwitch)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', position='150,100,0')
    sta2 = net.addStation('sta2', position='200,100,0')
    ap1 = net.addAccessPoint('ap1', ssid="simplewifi", mode="g", channel="5", position='170,100,0')
    ap2 = net.addAccessPoint('ap2', ssid="simplewifi", mode="g", channel="5", position='180,100,0')
    c0 = net.addController('c0', controller=Controller, ip='127.0.0.1', port=6633)
    s1 = net.addSwitch('s1')
    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating Stations"
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap2)
    net.addLink(ap1, s1)
    net.addLink(ap2, s1)
    print "*** Starting network"
    net.build()
    c0.start()
    ap1.start([c0])

    print "*** Building graph"
    net.plotGraph(max_x=300, max_y=300)

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

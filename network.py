#!/usr/bin/python

"""
This script parses a network traffic capture file (*.pcap) and creates
virtual nodes in mininet SDN.
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from scapy.all import *

def emptyNet():

    packets = rdpcap("data/android.pcap")
    nodes_ip = dict()

    for pkt in packets:
        if IP in pkt:
            s = pkt[IP].src
            d = pkt[IP].dst

            if (s not in nodes_ip):
                nodes_ip[s] = []
            if (d not in nodes_ip[s]):
                nodes_ip[s].append(d)

    n = list(nodes_ip)                #list of IP nodes
    print(n)

    "Create an empty network and add nodes to it."

    net = Mininet( controller=Controller )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding switch\n' )
    s3 = net.addSwitch( 's3' )

    info( '*** Adding hosts\n' )
    info( '*** Creating links\n' )
    #h = [] #Empty array for hosts
    for i in range(0,len(n)-1):
        print(n[i])
        i = net.addHost( str(i),ip=str(n[i]))
        net.addLink( i, s3)

    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()

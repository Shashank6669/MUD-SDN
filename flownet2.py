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
import Parse

     

def MudNet():
    

    "Create an empty network and add nodes to it."

    net = Mininet( controller=Controller )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding MUD Architecture Blocks\n' )
    hrs = net.addHost( 'RadServer', ip='10.0.0.1' )
    hms = net.addHost( 'MUDServer', ip='10.0.0.2' )
    hrc = net.addHost( 'RadClient', ip='10.0.0.3' )
    h1 = net.addHost( 'h1', ip='192.168.0.1', mac = '00:00:00:00:00:01' )  #Desktop connected to home network
    h2 = net.addHost( 'h2', ip='192.168.0.2', mac = '00:00:00:00:00:02' )  #IoT Device LED Light connected to home network
    h3 = net.addHost( 'h3', ip='', mac ='00:00:00:00:00:03' ) ####### IP address allowed for communication

    info( '*** Adding switch\n' )
    s3 = net.addSwitch( 's3' )
    s4 = net.addSwitch( 's4' )

    info( '*** Creating links\n' )
    net.addLink( hrs, s3 )
    net.addLink( hms, s3 )
    net.addLink( hrc, s3 )

    net.addLink( h1, s4 )
    net.addLink( h2, s4 )
    net.addLink( h3, s4 ) 

    
    info( '*** Starting network\n')
    net.start()

    hrs.cmdPrint('sudo radiusd -X > radbug.txt 2>&1 &')
    hrs.cmd('sleep 15')
    hms.cmdPrint('python -m SimpleHTTPServer 80 &')
    hms.cmd('sleep 5')
    hrc.cmdPrint('sudo echo "User-Name=Merkle, User-Password=MUDinmud, Cisco-MUD-URI=http://10.0.0.2/mud/lighting-example.json" | /usr/local/bin/radclient -x 10.0.0.1 auth testingMUD')
    #s3.cmdPrint('ifconfig')
    #net.stop()
    os.system("sleep 2")


################################################################################

    x,y = Parse.ACL()
    print('Inbound access entry: '+str(x))
    print('////////////////////////')
    print('Outbound access entry: '+str(y))
    
    net.get('h3').setIP(x[0])    
    
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



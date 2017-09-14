#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.

"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=Controller )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
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
    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()



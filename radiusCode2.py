#!/usr/bin/python

'This example shows how to work with Radius Server'

from mininet.net import Mininet, MininetWithControlNet
from mininet.node import  RemoteController, Controller, UserAP, UserSwitch, OVSSwitch, OVSAP
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import os
import time

class InbandController( RemoteController ):

    def checkListening( self ):
        "Overridden to do nothing."
        return

def topology():
    "Create a network."
    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSSwitch, accessPoint=OVSAP, enable_wmediumd=True, enable_interference=True )

    print "*** Creating nodes"
#    sta1 = net.addStation( 'sta1', radius_passwd='sdnteam', encrypt='wpa2', radius_identity='joe', position='110,120,0' )
    sta1 = net.addStation( 'sta1', radius_passwd='hello', encrypt='wpa2', radius_identity='bob', position='110,120,0' )
#    sta2 = net.addStation( 'sta2', radius_passwd='sdnteam', encrypt='wpa2', radius_identity='joe', position='200,100,0' )
    sta2 = net.addStation( 'sta2', radius_passwd='hello', encrypt='wpa2', radius_identity='bob', position='200,100,0' )
    h3 = net.addHost( 'h3', ip='192.168.0.1', mac='00:01:00:00:00:11' )
    h4 = net.addHost( 'h4', ip='192.168.0.10', mac='00:01:00:00:00:12' )
    h5 = net.addHost( 'h5', ip='192.168.0.11', mac='00:01:00:00:00:13' )
    ap1 = net.addAPAdhoc( 'ap1', ssid='simplewifi', protocols='OpenFlow10', radius_server='192.168.0.1', authmode='8021x', mode='a', channel='36', encrypt='wpa2', position='150,100,0' )
    s2 = net.addSwitch('s2', protocols='OpenFlow10')
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633 )

    print "*** Configuring Propagation Model"
    net.propagationModel("logDistancePropagationLossModel", exp=2.5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    net.addLink(s2, h3)
    net.addLink(ap1, s2)
    net.addLink(s2, h4)
    net.addLink(s2, h5)
    #ap1.cmdPrint('arp -s 10.0.0.3 00:01:00:00:00:11')

    print "*** Starting network"
    net.build()
    c0.start()
    s2.start( [c0] )

#    time.sleep(3)
#    os.system('ovs-ofctl add-flow s2 in_port=2,priority=65535,dl_type=0x800,nw_proto=17,tp_dst=1812,actions=1,controller')
    ap1.cmdPrint('ifconfig ap1-eth1 192.168.0.2')
    h3.cmdPrint('rc.radiusd start')
    #os.system('ovs-ofctl add-flow s2 in_port=2,priority=65535,dl_type=0x800,nw_proto=17,actions=1,controller')

    h4.cmd('route add -net 10.0.0.0/8 gw 192.168.0.2')
    h5.cmd('route add -net 10.0.0.0/8 gw 192.168.0.2')
    ap1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    sta1.cmd('route add -net 192.168.0.0/24 gw 10.0.0.6')
    sta2.cmd('route add -net 192.168.0.0/24 gw 10.0.0.6')

    #s2.cmd('dpctl unix:/tmp/s2 flow-mod table=0,cmd=add in_port=2,ip_dst=10.0.0.3,eth_type=0x800,ip_proto=17,udp_dst=1812 apply:set_field=ip_src:10.0.0.5,set_field=ip_dst:10.0.0.3,output=1')
    #s2.cmd('dpctl unix:/tmp/s2 flow-mod table=0,cmd=add in_port=1,ip_dst=10.0.0.5,eth_type=0x800,ip_proto=17 apply:set_field=ip_src:10.0.0.3,set_field=ip_dst:10.0.0.5,output=2')

    #s2.cmdPrint('dpctl add-flow unix:/tmp/s2 in_port=2,actions:output=1')
    #s2.cmdPrint('dpctl add-flow unix:/tmp/s2 in_port=1,actions:output=2')

    print "*** Building graph"
#    net.plotGraph(max_x=300, max_y=300)

    print "*** Running CLI"
    CLI( net )

    os.system('pkill radiusd')

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

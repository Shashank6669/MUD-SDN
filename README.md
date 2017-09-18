# MUD-SDN project summary:

This repository contains various versions of SDN topologies implemented for the IETF draft Manfacturer Usage Description acrchitecture. The SDN topologies are implemented in the network emulation software Mininet primarily and a fork of Mininet called Mininet-WiFi that includes WiFi functionalities and support for the RADIUS protocol. Mininet creates virtual linux namespaces for every node created in the network and can accurately emulate devices such as hosts, switches, routers, controllers etc. Mininet can be installed locally on Linux systems or on VMs. For more details regarding installation steps for Mininet and Mininet-WiFI, check out the following links:
1. Mininet: https://github.com/mininet/mininet
2. Mininet-WiFi: https://github.com/intrig-unicamp/mininet-wifi

The key component of the MUD architecture is the MUD file. It is a JSON file that defines the allowed communications for an IoT node in the network in the form of inbound and outbound access entries. These entries can be used to create an Access Control List that can be used to restrict the IoT device from communicating with undesirable endpoints. The idea of the MUD architecture proposal is that each IoT device will have a MUD file that is created, signed by the OEM and is stored in a secure MUD file server. The MUD files are given a URI and can be downloaded. When an IoT device requests to join a network, it emits an EAP packet with its credentials (certificates/username-password and MUD URI) to the network access gateway. The gateway verifies the credentials of the IoT device, encapsulates the EAP packet and sends a RADIUS request to the RADIUS server. The network access gateway plays the role of a RADIUS client. The RADIUS server verifies the authenticity of the RADIUS client, and then checks the credentials of the IoT device. If the IoT device is legitimate and has a valid MUD URI, the RADIUS server invokes the MUD controller to download the MUD JSON file from the MUD file server. 

Note:
1) The RADIUS server and MUD controller are considered to be in the same block. They can be decoupled if necessary.
2) There are other possibilities such as DHCP or LLDP that can be explored instead of RADIUS 

The MUD controller has the functionality to parse the JSON file and return it to the extracted ACL as a Cisco specified object to the RADIUS client, that is the network access gateway. For our implementation, a seperate code Parse.py is utilized to extract the ACL from the MUD JSON files. The code Parse.py works well for the MUD file "lighting-example.json" that has a single entry for inbound and outbound entries. It needs to be improved for working with multible entries in inbound and outbound directions. We consider simple network topologies with not more than six nodes at once. Hence we use the ACL for the IoT device as a major component to define the overall ACL for network. 

The ACL can be implemented using traditional Linux IPTables on each device. But this approach introduces scalability issues, ACL synchronization problems and manual network configuration difficulties. Hence, we consider using the concept of a SDN where the communication between network nodes is defined by flows. A flow can be losely defined as a path from path from a source to destination end points characterized by parameters such as IP address, MAC address, port numbers, protocol used ect. If a packet does not meet the criteria defined for a flow, it cannot traverse on that flow. The flow entries can also dictate when a packet should be dropped. So a flow typically has a matching rule criteria based on the source and destination parameters, and a corresponding action that needs to taken if a packet matches with specified flow criteria. Therefore, the flows can be used to create a comprehensive ACL for the entire network. A SDN can have multiple flow entries, stored hierarchially with a priority index in flow tables. Similarly, there can be multiple flow tables pipelined that implement various network policies. SDN offers the advantage of decoupling the two important network functions: routing and forwarding. The forwarding aspect is responsible for the switching action between different ingress and egress ports in a router/switch based on the route calculation performed in the network intelligence (CPU). The network intelligence is collectively placed in the SDN controller and is referred as the control plane. The forwarding functions performed exculsively by switching elements below compriseses the data plane. The interaction between the control plance and the data plane is facilitated by protocols such as OpenFLow. 

After a flow is defined, it is stored in an OpenFlow switch that supports the OpenFLow protocol. In a normal scenario for an SDN where an ACL is not of interrest, when a new packet matching an existing flow rule is encountered, the corresponding flow action is performed on the packet without any interaction with the controller. When a packet that does not match with any of the existing flows is encountered, it is encapsulated into a PACKET-IN OpenFlow message and sent to the controller. The controller analyzes the PACKET-IN message, and comes up with the required action such as finding a new route for the packet or a packet drop. This happens dynamically and a new flow rule is created. The details regarding the new flow rule are sent back to the OpenFLow switch as a PACKET-OUT message. But in the case of establishing an ACL, there is no necessity for creating dynamic flows if we know the network behaviour model beforehand. Hence, we can create appropriate flows that define the allowed communications and proactively install them on the network. This essentially means that we are setting up a predefined ACL. 

Using SDN offers the following advantages:
1) The centralized controller has virtually infinite resources for computation and complex routing functions since it's in the cloud
2) The controller can make globally optimum routing decisions rather than a hop-to-hop routing done by traditional routers
3) Centralization of high level network functionality improves programmability and easier customization of network features

Hence, for the following clear advantages, the ACL is implemented as flow tables in SDN rather than configuring each network node using traditional IPTables. 

The following section contains a basic explanation of the topology scenarios considered for various implementations in Mininet and Mininet-WiFi. The MUD architecture's implementation in Mininet contains three nodes including the RADIUS client, RADIUS server and the MUD file server. We need a separate node for the RADIUS client since the nodes in Mininet do not support the RADIUS protocol. Mininet-WiFi however, requires just two nodes in theory, one for the RADIUS server and another for the MUD file server. This is because Mininet-WiFi supports RADIUS protocol for the access points of the class UserAP. It is to be noted that the RADIUS server and the MUD file server can be run in the background in localhost as well. 

For all the SDN implementations with flow tables, only three nodes are considered to be part of the core network. 
1) A node for a desktop that needs to be secured from attacks if the IoT device in the same network is compromised. The desktop can communicate with a remote cloud server to control the IoT device indirectly using ICMP and TCP.  
2) An IoT device that can only talk to a remote cloude server through ICMP and TCP. It should not be allowed to access the desktop at any cost.
3) A remote cloud server that can thought of as a database server or a controller for the IoT device. It is a simple HTTP server that should be able to serve both the desktop and the IoT device. It is also able to initiate communication with both the devices on the home network. 

The flow tables for implementing the ACL for this know network topology is written in the text file tables.txt and is loaded onto the OpenFLow switch during execution.


1) Parse.py : Parses the MUD JSON file and returns the inbound and outbound access entries

2) Mudnet2.py : Implementation of MUD architecture with 3 nodes. A radius client, server and MUD file server. Under correct working conditions, the radius client should send a request to radius server, which in turn talks to the MUD file server after the authenticating the client and downloads the MUD file.

3) demo.py: Partially integrates the MUD architecture, parsing of downloaded MUD JSON file and translation of the extracted ACL into flow tables. The three aspects are written as three separate functions and are called sequentially. Takes into account of the difference in network IP addresses between the home network and the remote cloud server and incorporates NAT. 

4) demo1_1.py: Imports Parse.py for cleaner implementation of JSON parsing and overall integration.

5) demo2 is an unfinished version of demo.py with dynamic host addition.

6) demo3 is an unsuccessful attempt at using Mininet-Wifi with Freeradius

7) flownet2.py is the best version of the MUD-SDN architecture with 6 nodes, two switches and one controller. It includes all the required functions (MUD process, Parsing, SDN flow tables). 

                                        c0--------s3-------hrc
                                        |          | \
                                        |          |  \
                                h3----- s4       hms   hrs                     
                                        | \
                                        |  \
                                        h1  h2
                                        
h1: Desktop            hrc: Assumed to be the radius client since the s3 does not support RADIUS
h2: IoT Device         hrs: RADIUS server that is linked to the MUD-controller.py script
h3: Cloud server       hms: Simple HTTP server that servers up the MUD JSON file lighting-example.json


8) radcode is a working implementation of the Freeradius process in Mininet-WiFi.

9) demo4 is an implementation of flow tables based ACL in mininet-wifi. Does not involve the MUD architecture or parsing of MUD file.
       
    	                           c0
    	 	                          |
                     Sta1---AP2---s4---AP1---IoT
                                  |
                                 AP3
                                  |
                                 Sta2


10) demo5 is an implementation of flow tables based ACL with two APS and a host. Does not involve the MUD architecture or parsing of MUD file.

                                 c0
                                  |
                                 s4------AP1-----IoT
                                / \
                               /   \
                              h1    AP2
                                      \
                                   cloud server
         
11) radiusCode2.py is a combined implementation Freeradius and SDN using POX controller in Mininet-WiFi. It is provided by Ramon dos Reis Fontes (ramonrf@dca.fee.unicamp.br), part of the team that developed Mininet-WiFi. 

The combined implementation of the MUD architecture with SDN flowtables for ACL is yet to be achieved in Mininet-WiFi. The issues faced were majorly due to incompatibility in functionality between the UserAP access point class that offers support for RADIUS authentication process and the OVSAP class that offers OpenFlow OpenV Switch features for proactively loading the flow tables. Since only a single class of accesspoint could be utilized at once while running a topology, it was impossible to deploy a combined topology that utlizes all six nodes with access points of two different classes. 






















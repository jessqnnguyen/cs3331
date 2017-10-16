# CH4 Network Layer

* [ ] Overview and services it provides

* [ ] Structuring network layer packet delivery:
	* [ ] Datagram 
	* [ ] Virtual circuit model

* [ ] Fundamental role that addressing plays in delivering a packet to its destination host

* [ ] Packet forwarding on the internet 

* [ ] IP 

* [ ] Network-layer addressing and IPv4 datagram format

* [ ] Network address translation (NAT), datagram fragmentation, Internet Control Message Protocol, IPv6

Three major sections:
Network layer functions and services
Forwarding
Routing 


## Overview

The main role of the network layer is to move packets from a sending host to a receiving host.

To do so, 2 important network layer functions are used:

* Forwarding 
* Routing


### Fowarding

* A router-local action 
* When a packet arrives at a router's input link, the router must move the packet to the appropriate output link i.e. the next router which is on a path to the destination host
* Each router has a forwarding table
* A router forwards a packet by examining the arriving packet's header (usually the destination address of the packet) and then inserting that value as the key and the value as the output link the packet will be forwarded to 

![](network-layer-notes-01.png)

### Routing 

* A network wide process 
* Determines end-to-end paths that packets take from source to destination 





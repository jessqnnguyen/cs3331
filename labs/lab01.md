# Lab 1: Tools of the Trade

## Exercise 1

### Reachable hosts
* www.cse.unsw.edu.au
* compnet.epfl.ch - `14.3 % packet loss`
* www.intel.com.au
* www.telstra.com.au - `14.3 % packet loss`
* www.amazon.com 
* www.wikileaks.org
* www.tsinghua.edu.cn
* 8.8.8.8

### Unreachable hosts
* www.cancercouncil.org.au - `Request timeout`
* www.hola.hp - `cannot resolve: Unknown host`
* www.kremlin.ru - `Request timeout`

`www.cancercouncil.org.au` is not reachable via a browser or ping and appears to simply time out because it takes too long to wait for a reply from the host.

`www.hola.hp` is not reachable via a browser or ping and returns an unknown host error most likely because the host is down and a route doesn't exist for the destination host.

`www.kremlin.ru` appears to be reachable via a browser but not via ping most likely because the website has purposefully turned it off to avoid DoS attacks, otherwise known as the "Ping of death" or "Ping flood" in which an attacker overwhelms a network with excess ping packets which if successful consumes both outgoing and incoming bandwidth leading to network downtime.

## Exercise 2

1. There appears to be 23 routers between my workstation and `www.nyu.edu`. 5 routers along the path are part of the UNSW network.
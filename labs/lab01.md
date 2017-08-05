# CS3331 Lab 1: Tools of the Trade

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

### Question 1
#### Traceroute output
```
traceroute to www.nyu.edu (216.165.47.12), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.383 ms  0.370 ms  0.358 ms
 2  129.94.39.17 (129.94.39.17)  1.264 ms  1.240 ms  1.255 ms
 3  libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  8.239 ms ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.892 ms  1.874 ms
 4  libcr1-po-5.gw.unsw.edu.au (149.171.255.165)  1.433 ms ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  43.468 ms ombcr1-po-6.gw.unsw.edu.au (149.171.255.169)  43.403 ms
 5  unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.431 ms unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.497 ms unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.453 ms
 6  138.44.5.0 (138.44.5.0)  1.555 ms  1.391 ms  1.431 ms
 7  et-1-3-0.pe1.sxt.bkvl.nsw.aarnet.net.au (113.197.15.149)  2.122 ms  4.068 ms  4.058 ms
 8  et-0-0-0.pe1.a.hnl.aarnet.net.au (113.197.15.99)  96.909 ms  96.892 ms  96.883 ms
 9  et-2-1-0.bdr1.a.sea.aarnet.net.au (113.197.15.201)  147.976 ms  148.043 ms  147.933 ms
10  abilene-1-lo-jmb-706.sttlwa.pacificwave.net (207.231.240.8)  148.027 ms  148.023 ms  148.008 ms
11  et-4-0-0.4079.sdn-sw.miss2.net.internet2.edu (162.252.70.0)  158.735 ms  159.074 ms  157.868 ms
12  et-4-0-0.4079.sdn-sw.minn.net.internet2.edu (162.252.70.58)  180.348 ms  180.312 ms  180.407 ms
13  et-7-0-0.4079.sdn-sw.eqch.net.internet2.edu (162.252.70.106)  188.062 ms  188.126 ms  188.160 ms
14  et-4-1-0.4079.rtsw.clev.net.internet2.edu (162.252.70.112)  196.808 ms  196.921 ms  197.151 ms
15  buf-9208-I2-CLEV.nysernet.net (199.109.11.33)  201.168 ms  201.139 ms  201.140 ms
16  syr-9208-buf-9208.nysernet.net (199.109.7.193)  205.254 ms  205.171 ms  205.318 ms
17  nyc-9208-syr-9208.nysernet.net (199.109.7.162)  210.123 ms  213.722 ms  213.714 ms
18  199.109.5.6 (199.109.5.6)  210.518 ms  210.608 ms  210.748 ms
19  DMZGWA-PTP-EXTGWA.NET.NYU.EDU (128.122.254.65)  211.111 ms  211.034 ms  211.112 ms
20  NYUGWA-PTP-DMZGWA-NGFW.NET.NYU.EDU (128.122.254.108)  230.657 ms  224.863 ms  224.808 ms
21  NYUFW-OUTSIDE-NGFW.NET.NYU.EDU (128.122.254.116)  211.306 ms  211.199 ms  211.282 ms
22  * * *
23  WSQDCGWA-VL902.NET.NYU.EDU (128.122.1.38)  211.609 ms  211.935 ms  211.858 ms
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```
#### Answer
There appears to be 23 routers between my workstation and `www.nyu.edu`. 5 routers along the path are part of the UNSW network. Between routers 11 - `et-4-0-0.4079.sdn-sw.miss2.net.internet2.edu (162.252.70.0)` - and 12 - `et-4-0-0.4079.sdn-sw.minn.net.internet2.edu (162.252.70.58)` - do the packets appear to cross the Pacific Ocean since there appears to be a significantly larger average RTT between these two routers than between the previous routers which have only been about 10 ms difference apart while the RTT between these two routers was ~23 ms.

### Question 2
#### Traceroute output
##### Traceroute to www.ucla.edu
```
traceroute to www.ucla.edu (164.67.228.152), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.129 ms  0.126 ms  0.171 ms
 2  129.94.39.17 (129.94.39.17)  1.083 ms  1.030 ms  1.230 ms
 3  ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.684 ms libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  3.627 ms ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  2.609 ms
 4  libcr1-po-5.gw.unsw.edu.au (149.171.255.165)  1.446 ms ombcr1-po-6.gw.unsw.edu.au (149.171.255.169)  1.487 ms ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.426 ms
 5  unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.456 ms  1.477 ms  1.492 ms
 6  138.44.5.0 (138.44.5.0)  1.573 ms  1.629 ms  1.612 ms
 7  et-1-3-0.pe1.sxt.bkvl.nsw.aarnet.net.au (113.197.15.149)  2.601 ms  4.037 ms  3.978 ms
 8  et-0-0-0.pe1.a.hnl.aarnet.net.au (113.197.15.99)  95.629 ms  95.621 ms  95.645 ms
 9  et-2-1-0.bdr1.a.sea.aarnet.net.au (113.197.15.201)  146.861 ms  146.813 ms  146.793 ms
10  cenichpr-1-is-jmb-778.snvaca.pacificwave.net (207.231.245.129)  163.551 ms  163.558 ms  163.517 ms
11  hpr-lax-hpr3--svl-hpr3-100ge.cenic.net (137.164.25.73)  172.240 ms  172.359 ms  172.356 ms
12  * * *
13  bd11f1.anderson--cr00f2.csb1.ucla.net (169.232.4.4)  171.953 ms bd11f1.anderson--cr001.anderson.ucla.net (169.232.4.6)  171.508 ms  171.482 ms
14  cr00f1.anderson--dr00f2.csb1.ucla.net (169.232.4.55)  171.363 ms cr00f2.csb1--dr00f2.csb1.ucla.net (169.232.4.53)  171.558 ms  171.550 ms
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```
##### Traceroute to www.u-tokyo.ac.jp
```
traceroute to www.u-tokyo.ac.jp (210.152.135.178), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.379 ms  0.371 ms  0.359 ms
 2  129.94.39.17 (129.94.39.17)  1.246 ms  1.240 ms  1.229 ms
 3  ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.963 ms  1.928 ms libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.779 ms
 4  ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.412 ms libcr1-po-6.gw.unsw.edu.au (149.171.255.201)  1.447 ms libcr1-po-5.gw.unsw.edu.au (149.171.255.165)  1.418 ms
 5  unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.464 ms  1.485 ms  1.503 ms
 6  138.44.5.0 (138.44.5.0)  1.608 ms  1.435 ms  1.350 ms
 7  et-0-3-0.pe1.bkvl.nsw.aarnet.net.au (113.197.15.147)  3.323 ms  2.125 ms  2.087 ms
 8  ge-4_0_0.bb1.a.pao.aarnet.net.au (202.158.194.177)  156.757 ms  156.850 ms  156.824 ms
 9  paloalto0.iij.net (198.32.176.24)  158.627 ms  158.648 ms  158.574 ms
10  osk004bb01.IIJ.Net (58.138.88.189)  271.904 ms  271.972 ms  271.930 ms
11  osk004ix51.IIJ.Net (58.138.106.126)  290.736 ms  290.715 ms osk004ix51.IIJ.Net (58.138.106.130)  281.087 ms
12  210.130.135.130 (210.130.135.130)  322.247 ms  321.291 ms  321.286 ms
13  124.83.228.93 (124.83.228.93)  290.519 ms  283.366 ms  309.060 ms
14  124.83.228.74 (124.83.228.74)  271.650 ms  271.815 ms  281.254 ms
15  124.83.252.242 (124.83.252.242)  288.793 ms  288.814 ms  288.831 ms
16  158.205.134.22 (158.205.134.22)  279.214 ms  279.172 ms  279.223 ms
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```
##### Traceroute to www.lancaster.ac.uk
```
traceroute to www.lancaster.ac.uk (148.88.2.80), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.380 ms  0.375 ms  0.363 ms
 2  129.94.39.17 (129.94.39.17)  1.330 ms  1.302 ms  1.280 ms
 3  libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.641 ms ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.761 ms  1.993 ms
 4  ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.522 ms ombcr1-po-6.gw.unsw.edu.au (149.171.255.169)  1.553 ms ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.556 ms
 5  unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.585 ms  1.527 ms  1.584 ms
 6  138.44.5.0 (138.44.5.0)  1.641 ms  1.442 ms  1.447 ms
 7  et-1-3-0.pe1.sxt.bkvl.nsw.aarnet.net.au (113.197.15.149)  2.340 ms  2.493 ms  2.483 ms
 8  et-0-0-0.pe1.a.hnl.aarnet.net.au (113.197.15.99)  95.245 ms  95.469 ms  95.408 ms
 9  et-2-1-0.bdr1.a.sea.aarnet.net.au (113.197.15.201)  146.719 ms  146.680 ms  146.659 ms
10  abilene-1-lo-jmb-706.sttlwa.pacificwave.net (207.231.240.8)  147.343 ms  147.311 ms  147.350 ms
11  et-4-0-0.4079.sdn-sw.miss2.net.internet2.edu (162.252.70.0)  157.512 ms  157.509 ms  157.636 ms
12  et-4-0-0.4079.sdn-sw.minn.net.internet2.edu (162.252.70.58)  180.860 ms  180.704 ms  180.644 ms
13  et-7-0-0.4079.sdn-sw.eqch.net.internet2.edu (162.252.70.106)  189.741 ms  188.456 ms  199.316 ms
14  et-4-1-0.4079.rtsw.clev.net.internet2.edu (162.252.70.112)  197.009 ms  197.165 ms  197.155 ms
15  et-2-0-0.4079.sdn-sw.ashb.net.internet2.edu (162.252.70.54)  204.675 ms  204.635 ms  204.549 ms
16  et-4-1-0.4079.rtsw.wash.net.internet2.edu (162.252.70.65)  204.776 ms  204.955 ms  204.925 ms
17  internet2.mx1.lon.uk.geant.net (62.40.124.44)  279.595 ms  279.615 ms  279.607 ms
18  janet-gw.mx1.lon.uk.geant.net (62.40.124.198)  279.774 ms  279.648 ms  279.649 ms
19  ae29.londpg-sbr2.ja.net (146.97.33.2)  285.777 ms  285.776 ms  285.760 ms
20  ae31.erdiss-sbr2.ja.net (146.97.33.22)  284.152 ms  284.144 ms  284.118 ms
21  ae29.manckh-sbr1.ja.net (146.97.33.42)  285.781 ms  285.791 ms  285.842 ms
22  cnl.manckh-sbr1.ja.net (146.97.41.54)  288.149 ms  288.042 ms  288.495 ms
23  * * *
24  ismx-issrx.rtr.lancs.ac.uk (148.88.255.17)  289.874 ms  289.473 ms  289.792 ms
25  dc.iss.srv.rtrcloud.lancs.ac.uk (148.88.253.3)  310.623 ms  307.690 ms  307.699 ms
26  www-ha.lancs.ac.uk (148.88.2.80)  289.755 ms !X  289.523 ms !X  289.294 ms !X
```

#### Answer
The path of my machine to these three destinations seem to diverge at a router with the IP address `138.44.5.0`. Upon running the `whois` command on this router, this router appears to be called AARNET which stands for the Australian Academic and Research Network. The number of hops along each path also appears to be proportional to the physical distance from my computer to the destination, that is, the greater the distance, the more hops it takes to reach the destination. For example the first destination is bound for LA, ~12087 km away from Sydney. The second destination is bound for somewhere in Japan, ~7915 km away from Sydney. The third destination is bound for Lancaster in the UK, ~17008 km away.

Destination | Approximate distance from my computer | Hops taken to reach destination
------------ | ------------- | ------------
1 | 12087 km  | 14
2 | 7915 km | 16
3 | 17008 km | 26

### Question 3

#### Traceroute output

##### From my machine to www.speedtest.com.sg
```
traceroute to www.speedtest.com.sg (202.150.221.170), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.189 ms  0.178 ms  0.167 ms
 2  129.94.39.17 (129.94.39.17)  1.052 ms  1.077 ms  1.069 ms
 3  ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.625 ms libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.790 ms  1.520 ms
 4  ombcr1-po-6.gw.unsw.edu.au (149.171.255.169)  1.240 ms ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.309 ms libcr1-po-5.gw.unsw.edu.au (149.171.255.165)  1.196 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.353 ms  1.390 ms unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.441 ms
 6  138.44.5.0 (138.44.5.0)  1.419 ms  1.389 ms  1.394 ms
 7  et-0-3-0.pe1.alxd.nsw.aarnet.net.au (113.197.15.153)  1.709 ms  1.794 ms  1.796 ms
 8  xe-0-0-3.pe1.wnpa.akl.aarnet.net.au (113.197.15.67)  24.261 ms xe-0-2-1-204.pe1.wnpa.alxd.aarnet.net.au (113.197.15.183)  24.285 ms xe-0-0-3.pe1.wnpa.akl.aarnet.net.au (113.197.15.67)  24.216 ms
 9  et-0-1-0.200.pe1.tkpa.akl.aarnet.net.au (113.197.15.69)  24.595 ms  24.496 ms  24.536 ms
10  xe-0-2-6.bdr1.a.lax.aarnet.net.au (202.158.194.173)  147.995 ms  147.986 ms  147.963 ms
11  singtel.as7473.any2ix.coresite.com (206.72.210.63)  309.517 ms  309.410 ms  309.446 ms
12  203.208.171.117 (203.208.171.117)  310.748 ms 203.208.172.173 (203.208.172.173)  305.897 ms 203.208.158.29 (203.208.158.29)  328.607 ms
13  203.208.154.45 (203.208.154.45)  331.657 ms 203.208.182.125 (203.208.182.125)  358.598 ms 203.208.173.73 (203.208.173.73)  363.128 ms
14  203.208.171.198 (203.208.171.198)  338.623 ms 203.208.182.45 (203.208.182.45)  327.320 ms 203.208.171.198 (203.208.171.198)  338.630 ms
15  203.208.177.110 (203.208.177.110)  334.582 ms  322.519 ms  336.447 ms
16  202-150-221-170.rev.ne.com.sg (202.150.221.170)  328.271 ms  337.710 ms  328.535 ms
```
##### From www.speedtest.com.sg back to my machine

##### From my machine to www.telstra.net/cgi-bin/trace 

##### From www.telstra.net/cgi-bin/trace to my machine


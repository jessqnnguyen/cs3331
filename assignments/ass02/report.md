# Assignment 2 Report

## Network topology representation

I've used solely Python dictionaries to implement an extremely light-weight representation of the network topology.

* I created 2 dictionaries - one called `g` and one called `e`.

* `g` stores just the connections in the graph in key, value pairs using Python's dictionary class. An entry in `g` looks something like this:

```
 ("A", ["B", "C"])
```
* This represents that there exists a node called "A" in the network which has neighbouring nodes "B" and "C"
* `e` stores each link's data including it's propagation delay, maximum capacity and also the current number of reservations on the link. An entry in `e` looks something like this:

```
('AC', (15, 10, 0))

```
* This represents the link between node "A" and node "C" has a propagation delay of 15, maximum capacity of 10 units per link and currently 0 reservations on the link.

## Performance metrics 

Comparison of the three routing protocols when run with sample `topology.txt` and `workload.txt` inputs and a packet rate of 2.

### Virtual circuit network

Performance Metrics                              | SHP       | SDP        | LLP
-------------------------------------------------|-----------|------------|-----
Total number of virtual circuit requests         | 5884      | 5884       | 5884
Total number of packets                          | 355091    | 355091     | 355091
Number of successfully routed packets            | 315336    | 322553     | 352005
Percentage of successfully routed packets        | 88.804278 | 90.836715  | 99.130927
Number of blocked packets                        | 39755     | 32538      | 3086
Percentage of blocked packets                    | 11.195722 | 9.163285   | 0.869073
Average number of hops per circuit               | 3.65      | 4.31       | 4.82
Average cumulative propagation delay per circuit | 171.55    | 141.17     | 236.6

### Packet network

Performance Metrics                              | SHP       | SDP        | LLP
-------------------------------------------------|-----------|------------|-----
Total number of virtual circuit requests         | 5884      | 5884       | 5884
Total number of packets                          | 355091    | 355091     | 355091
Number of successfully routed packets            | 304502    | 308239     | -
Percentage of successfully routed packets        | 85.753229 | 86.805636  | -
Number of blocked packets                        | 50589     | 46852      | -
Percentage of blocked packets                    | 14.246771 | 13.194364  | -
Average number of hops per circuit               | 3.6       | 4.21       | -
Average cumulative propagation delay per circuit | 167.89    | 140.9      | -


## Analysis of results

From the virtual circuit network table, clear patterns on the following performance metrics:

* `Percentage of blocked packets`
* `Average number of hops per circuit` 
* `Average cumulative propagation` 

can be seen from running the network with different routing algorithms. 

### Percentage of blocked packets

* The percentage of blocked packets is at it's lowest when the program is run with LLP at 0.86%. 

* This is because LLP alogrithm optimises to find the path that has the minimum maximum (number of reservations on the link / link's capacity), that is to find the path with the minimum value at it's major bottlehead point. 

* As a result, running LLP naturally minimises the number of blocked packets in comparison to SHP and SDP since by choosing the path that minimises the maximum amount of congestion that a packet will experience at any link on the path, also minimises the chance that it will be blocked due to congestion.

* Meanwhile, SDP can be seen to generally perform slightly better than SHP at 9.16% vs. 11.20%. 

* This is because it selects the path with the least delay which leads to a slightly greater chance of it selecting a larger variety of alternate paths that are not blocked compared to SHP. 

* This is because SHP optimises on minimum number of hops required and as a result is more likely to select the same path for multiple circuit requests in order to minimise the number of hops required to get there.

### Average number of hops per circuit

* The average number of hops is at it's lowest when the program is run with SHP at 3.65 average number of hops per circuit

* As mentioned in the previous section, this is clearly because SHP optimises to find a path with the minimum number of hops so will always perform better than SDP and LLP on this performance metric

* Meanwhile, SDP can be seen to perform better at 4.31 hops per circuit vs. LLP's 4.82 average number of hops per circuit. This is most likely because SDP optimises for less delay and naturally will select paths that are shorter than LLP while LLP selects path irregardless and only takes into account congestion on the path 

### Average cumulative propagation delay

* SDP clearly performs the best at this performanc metric at an average cumulative propagation delay of 141.17 ms 

* This is because SDP selects the path with the least cumulative delay along all the links in the path and hence will always select paths with the least delay, naturally resulting in a less average cumulative propagation delay

* Meanwhile SHP performs slightly better at an average of 171.55 ms compared to LLP's 236.6 ms

* This is most likely because SHP selects the path with the least hops so therefore less delays will be accumulate since it's a shorter path than the path LLP selects which optimises for less congestion and increased likelihood of the packet actually reaching the destination rather than speed

### Overall

Note that overall, while it is clear SHP performs the best at `Average number of hops per circuit`, SDP performs best at `Average cumulative propagation delay` and LLP performs best at `Percentage of blocked packets` there is a little bit of randomness whether for example SDP or SHP performs better at `Percentage of blocked packets` due to paths breaking ties when the routing algorithms computes the path.

Hence while generally it is the case that in:

* Average number of hops per circuit - SHP < SDP < LLP 
* Average cumulative propagation delay - SDP < SHP < LLP
* Percentage of blocked packets - LLP < SDP < SHP 

The second 'less than' operator arguments can be often be reordered due to randomness in breaking ties.











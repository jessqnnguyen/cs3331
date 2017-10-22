import sys
import string
import re
from datetime import datetime
import math
import queue
import statistics

def main(argv):
    # network_scheme = argv[1] # "CIRCUIT" or "PACKET"
    # routing_scheme = argv[2] # "SHP" "SDP" or "LLP"
    topology_file = argv[1]
    workload_file = argv[2]
    packet_rate = int(argv[3]) # positive num, packets / sec

    num_vc_requests = 0
    num_total_packets = 0
    num_successfully_routed_packets = 0
    num_blocked_packets = 0
    hops = [] # Store all the hop numbers to avg out at the end
    prop_delays = []

    # Process the topology file and store the graph
    g = dict()
    e = dict() # edge to a tuple of (d, c, curr_capacity)
               # e.g. Initially, e[AB] = 10, 19, 0
    f = open(topology_file)
    line = f.readline()

    while line:
        line_args = str.split(line, ' ')
        n1 = line_args[0]
        n2 = line_args[1]
        d = line_args[2]
        c = line_args[3].rstrip()
        # print(n1 + " " + n2 + " " + str(d) + " " + str(c))
        add_edge(g, e, n1, n2, d, c)
        add_edge(g, e, n2, n1, d, c)
        line = f.readline()

    f.close()

    for k, v in sorted(g.items()):
        print(k, v)

    for k,v in sorted(e.items()):
        print(k, v)

    # Process the workload file and store the requests
    requests = dict()

    f = open(workload_file)
    line = f.readline()
    while line:
        line_args = str.split(line, ' ')
        time = line_args[0]
        src = line_args[1]
        dest = line_args[2]
        ttl = line_args[3].rstrip()
        # print(str(n) + " " + str(time) + " " + src + " " + dest + " " + str(ttl))
        add_request(requests, time, src, dest, ttl)
        line = f.readline()
    f.close()

    for k,v in sorted(requests.items()):
        print(k, v)

    # Process the requests in timestamp order
    for k, v in sorted(requests.items()):
        num_vc_requests += 1
        src = v[0]
        dest = v[1]
        ttl = float(v[2])
        packets_to_send = math.floor(float(packet_rate * ttl))
        num_total_packets += packets_to_send
        path = find_shortest_path(g, e, src, dest)
        if check_capacity:
            establish_circuit(e, path)
            num_successfully_routed_packets += packets_to_send
            hops.append(len(path))
            path_delay = compute_prop_delay(e, path)
            prop_delays.append(path_delay)
        else:
            num_blocked_packets += packets_to_send
    # path = find_shortest_path(g, e, "A", "D")
    # print(str(path))
    #
    # print("is path ok? " + str(check_capacity(e, path)))
    # if check_capacity:
    #     establish_circuit(e, path)
    #     print(e)

    percentage_successfully_routed_packets = (num_successfully_routed_packets/num_total_packets) * 100
    percentage_blocked_packets = (num_blocked_packets/num_total_packets) * 100
    # total = 0
    # for hop_num in hops:
    #     total += hop_num
    # avg_num_hops = total / len(hops)
    avg_num_hops = statistics.mean(hops)

    cumulative_average_prop_delays = []
    i = 1
    curr_sum = 0
    for delay in prop_delays:
        curr_sum += delay
        cumulative_average_prop_delays.append(curr_sum / i)
        i += 1

    average_cumulative_prop_delay = statistics.mean(cumulative_average_prop_delays)

    print("total number of virtual connection requests: " + str(num_vc_requests))
    print("total number of packets: " + str(num_total_packets))
    print("number of successfully routed packets: " + str(num_successfully_routed_packets))
    print("percentage of successfully routed packets " +  str(percentage_successfully_routed_packets))
    print("number of blocked packets: " + str(num_blocked_packets))
    print("percentage of blocked packets: " + str(percentage_blocked_packets))
    print("average number of hops per circuit: " + str(avg_num_hops))
    print("average cumulative propagation delay per circuit: " + str(average_cumulative_prop_delay))

def compute_prop_delay(e, path):
    total_delay = 0
    for i in range(0, len(path) - 1):
        curr_link = path[i] + path[i + 1]
        (prop_delay, max_capacity, curr_capacity) = e[curr_link]
        total_delay += prop_delay
    return total_delay

def check_capacity(e, path):
    isPathOK = True
    for i in range(0, len(path) - 1):
        curr_link = path[i] + path[i + 1]
        (prop_delay, max_capacity, curr_capacity) = e[curr_link]
        if curr_capacity == max_capacity:
            isPathOK = False
    return isPathOK

def establish_circuit(e, path):
    for i in range(0, len(path) - 1):
        curr_link1 = path[i] + path[i + 1] # e.g. AB
        curr_link2 = path[i + 1] + path[i] # e.g. BA
        (prop_delay, max_capacity, curr_capacity) = e[curr_link1]
        e[curr_link1] = (prop_delay, max_capacity, curr_capacity + 1)
        e[curr_link2] = (prop_delay, max_capacity, curr_capacity + 1)



def find_shortest_path(g, e, src, dest):
    (dist, st) = dijkstra(g, e, src, dest)
    path = []
    while True:
        path.append(dest)
        if dest == src:
            break
        dest = st[dest]
    path.reverse()
    return path

def dijkstra(g, e, src, dest):
    dist = dict() # final distances
    dist[src] = 0
    st = dict() # previous node in optimal path from src
    q = queue.PriorityQueue()
    if src not in g:
        raise TypeError("The source node doesn't exist in the graph!")
    if dest not in g:
        raise TypeError("The destination node doesn't exist in the graph!")
    if src == dest:
        st[dest] = src
        dist[dest] = 0
    else:
        for v in g.keys():
            if v != src:
                dist[v] = float("inf")
                st[v] = ""

        q.put((dist[src], src))
        while (not q.empty()):
            # remove and return the best vertex
            (d, u) = q.get()
            print ("u = " + str(u))
            if u == dest:
                break
            for v in g[u]:
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    st[v] = u
                    q.put((dist[v], v))
    return (dist, st)

def add_request(requests, time, src, dest, ttl):
    requests[float(time)] = (src, dest, ttl)

def add_edge(g, e, n1, n2, d, c):
    if not n1 in g:
        g.setdefault(n1, [])
    g[n1].append(n2)
    key = n1 + n2
    e[key] = (int(d), int(c), 0)


if __name__ == "__main__":
    # sys.stdout = sys.stderr
    main(sys.argv)

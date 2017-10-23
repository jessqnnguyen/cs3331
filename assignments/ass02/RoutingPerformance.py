import sys
import string
import re
from datetime import datetime
import math
import queue
import statistics

def main(argv):
    # network_scheme = argv[1] # "CIRCUIT" or "PACKET"
    routing_scheme = argv[1] # "SHP" "SDP" or "LLP"
    topology_file = argv[2]
    workload_file = argv[3]
    packet_rate = int(argv[4]) # positive num, packets / sec

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
    request_timestamps = []

    f = open(workload_file)
    line = f.readline()
    while line:
        num_vc_requests += 1
        line_args = str.split(line, ' ')
        time = line_args[0]
        src = line_args[1]
        dest = line_args[2]
        ttl = line_args[3].rstrip()
        # print(str(n) + " " + str(time) + " " + src + " " + dest + " " + str(ttl))
        add_request(requests, time, src, dest, ttl)
        start_time = round(float(time), 1)
        request_timestamps.append(start_time)
        end_time = round(float(time) + float(ttl), 1)
        request_timestamps.append(end_time)
        line = f.readline()
    f.close()

    print("request_timestamps size =  " + str(len(request_timestamps)))
    # for k,v in sorted(requests.items()):
    #     print(k, v)

    request_timestamps.sort()
    print(request_timestamps)
    curr_request_num = 0
    next_request_time = request_timestamps[curr_request_num]
    t = next_request_time

    jobs = queue.PriorityQueue()

    print("requests size = " + str(requests.items()))

    for k, v in sorted(requests.items()):
        for r in v:
            print("r : " + str(r))
            (src, dest, ttl) = r
            addr = (src, dest)
            path = find_shortest_path(g, e, src, dest, routing_scheme)
            jobs.put((k, addr, path, "allocate"))
            deallocate_timestamp = k + ttl
            jobs.put((deallocate_timestamp, addr, path, "deallocate"))

    print("queue size: " + str(jobs.qsize()))
    # while not(jobs.empty()):
    #     job = jobs.get()
    #     print(job)
    # Add jobs to the queue from the requests
    while not(jobs.empty()):
        print("t =  " + str(t))
        print("next request time = " + str(next_request_time))
        print ("curr_request_num =  " + str(curr_request_num))
        if t == next_request_time:
            for i in range(curr_request_num, len(request_timestamps)):
                timestamp = request_timestamps[i]
                print("curr timestamp checking =  " + str(timestamp))
                if timestamp == t:
                    print ("next request time event registered")
                    (timestamp, addr, path, job_type) = jobs.get()
                    print("queue size now = " + str(jobs.qsize()))
                    print("current job processsing %s %s" % (timestamp, job_type))
                    curr_request_num += 1
                    if curr_request_num < len(request_timestamps):
                        next_request_time = request_timestamps[curr_request_num]
                    src = addr[0]
                    dest = addr[1]
                    print ("addr: " + str(addr))
                    # ttl = float(v[2])
                    if job_type == "allocate":
                        print("allocating")
                        print("e: " + str(e))
                        print("checking capacity... " + str(check_capacity(e, path)))
                        packets_to_send = math.floor(float(packet_rate * ttl))
                        num_total_packets += packets_to_send
                        if check_capacity(e, path):
                            establish_circuit(e, path)
                            num_successfully_routed_packets += packets_to_send
                            hops.append(len(path))
                            path_delay = compute_prop_delay(e, path)
                            prop_delays.append(path_delay)
                        else:
                            print("blocked")
                            num_blocked_packets += packets_to_send
                    elif job_type == "deallocate":
                        print("deallocating")
                        terminate_circuit(e, path)
        t = round((t + 0.1), 1)

    # path = find_shortest_path(g, e, "A", "D")
    # print(str(path))
    #
    # print("is path ok? " + str(check_capacity(e, path)))
    # if check_capacity:
    #     establish_circuit(e, path)
    #     print(e)

    percentage_successfully_routed_packets = (num_successfully_routed_packets/num_total_packets) * 100
    percentage_blocked_packets = (num_blocked_packets/num_total_packets) * 100
    total = 0
    for hop_num in hops:
        total += hop_num
    avg_num_hops = total / len(hops)
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

def process_next_job():
    (timestamp, v) = jobs.get()
    src = v[0]
    dest = v[1]
    ttl = float(v[2])
    packets_to_send = math.floor(float(packet_rate * ttl))
    num_total_packets += packets_to_send
    path = find_shortest_path(g, e, src, dest, routing_scheme)
    if check_capacity:
        establish_circuit(e, path)
        num_successfully_routed_packets += packets_to_send
        hops.append(len(path))
        path_delay = compute_prop_delay(e, path)
        prop_delays.append(path_delay)
    else:
        num_blocked_packets += packets_to_send

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

def terminate_circuit(e, path):
    for i in range(0, len(path) - 1):
        curr_link1 = path[i] + path[i + 1] # e.g. AB
        curr_link2 = path[i + 1] + path[i] # e.g. BA
        (prop_delay, max_capacity, curr_capacity) = e[curr_link1]
        e[curr_link1] = (prop_delay, max_capacity, curr_capacity - 1)
        e[curr_link2] = (prop_delay, max_capacity, curr_capacity - 1)

def find_shortest_path(g, e, src, dest, protocol):
    if protocol == "SHP":
        (dist, st) = dijkstra_shp(g, e, src, dest)
    if protocol == "SDP":
        (dist, st) = dijkstra_sdp(g, e, src, dest)
    if protocol == "LLP":
        (dist, st) = dijkstra_llp(g, e, src, dest)
    path = []
    while True:
        path.append(dest)
        if dest == src:
            break
        dest = st[dest]
    path.reverse()
    return path

def dijkstra_llp(g, e, src, dest):
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
            # print ("u = " + str(u))
            if u == dest:
                break
            for v in g[u]:
                link = u + v
                (d, c, cc) = e[link]
                link_load = (cc / c)
                alt = link_load
                if alt < dist[v]:
                    dist[v] = alt
                    st[v] = u
                    q.put((dist[v], v))
    return (dist, st)

def dijkstra_sdp(g, e, src, dest):
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
            # print ("u = " + str(u))
            if u == dest:
                break
            for v in g[u]:
                link = u + v
                (d, c, cc) = e[link]
                alt = dist[u] + d
                if alt < dist[v]:
                    dist[v] = alt
                    st[v] = u
                    q.put((dist[v], v))
    return (dist, st)

def dijkstra_shp(g, e, src, dest):
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
            # print ("u = " + str(u))
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
    key = float(time)
    val = (src, dest, float(ttl))
    if not key in requests:
        requests.setdefault(key, [])
    requests[key].append(val)

def add_edge(g, e, n1, n2, d, c):
    if not n1 in g:
        g.setdefault(n1, [])
    g[n1].append(n2)
    key = n1 + n2
    e[key] = (int(d), int(c), 0)


if __name__ == "__main__":
    # sys.stdout = sys.stderr
    main(sys.argv)

import sys
import string
import re

def main(argv):
    # network_scheme = argv[1] # "CIRCUIT" or "PACKET"
    # routing_scheme = argv[2] # "SHP" "SDP" or "LLP"
    topology_file = argv[1]
    # workload_file = argv[4]
    # packet_rate = int(argv[5]) # positive num, packets / sec

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
        print(n1 + " " + n2 + " " + str(d) + " " + str(c))
        add_edge(g, e, n1, n2, d, c)
        add_edge(g, e, n2, n1, d, c)
        line = f.readline()

    f.close()

    for k, v in sorted(g.items()):
        print(k, v)

    for k,v in sorted (e.items()):
        print(k, v)

def add_edge(g, e, n1, n2, d, c):
    if not n1 in g:
        g.setdefault(n1, [])
    g[n1].append(n2)
    key = n1 + n2
    e[key] = (d, c, 0)


if __name__ == "__main__":
    # sys.stdout = sys.stderr
    main(sys.argv)

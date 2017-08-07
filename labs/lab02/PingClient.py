# Retrieve command line args library.
import sys
# Socket programming library.
import socket
# Retrieve system time library.
from datetime import datetime

# Store input server parameters - host and port to ping to.
host = sys.argv[1]
port = sys.argv[2]
serverAddr = (host, int(port))
bufferSize = 2048

# Create a UDP socket instance using IPv4 addresses (AF_INET) and
# TCP protocol (SOCK_DGRAM).
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ping the server.
for i in range(0, 9):
    # Save current time stamp.
    timestamp = datetime.now()
    # Store ping message to send to server.
    message = "ping to %s, seq = %d, timestamp = %s" % (host, i, str(timestamp))
    try:
        # Wait for up to one second for a reply.
        s.settimeout(1)
        # Send message to the server.
        sent = s.sendto(message, serverAddr)
        # Store reply from server.
        reply = s.recv(bufferSize)
        # Calculate rtt.
        delta = datetime.now() - timestamp
        rtt = delta.microseconds
        print "ping to %s, seq = %d, rtt = %d ms" % (host, i, rtt)
    except:
        continue

# Close the socket.
s.close()

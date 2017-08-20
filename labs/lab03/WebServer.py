# Retrieve command line args library.
import sys
# Socket programming library.
import socket

import string
import re

# Retrieve server port from command line input args.
# port = sys.argv[1]
port = int (sys.argv[1])
host = ''

# Store default buffer size (max amount of data to receive at once).
bufferSize = 1024

# Create a TCP socket (SOCK_STREAM) and bind it to the input port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

while True:
    conn, address = s.accept()
    # Retrieve the request object
    data = conn.recv(bufferSize)
    lines = string.split(data, '\n')
    match = re.findall('/.[a-zA-Z0-9]+.[a-z]+', data)[0]
    fileName = re.findall('[a-zA-Z0-9_]+.[a-zA-Z0-9_]+', match)[0]
    try:
        f = open(fileName, 'rb')
        l = f.read(bufferSize)
        conn.send('HTTP/1.0 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('\n')
        conn.send('"""')
        while l:
            conn.send(l)
            print "Sent: %s" % l
            l = f.read(bufferSize)
        conn.send('"""')
        f.close()
    except IOError:
        conn.send("HTTP/1.1 404 Not Found\r\n\r\n")

conn.close()

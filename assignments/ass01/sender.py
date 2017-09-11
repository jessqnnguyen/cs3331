""" Sender operating on the STP Protocol module. """
import sys
# Socket programming library.
import socket
# Object serialization library.
import pickle
# System time library for logging.
from datetime import datetime
# Segment module.
from segment import STPSegment, STPLogger

LOG_FILE_NAME = "Sender_log.txt"
STP_LOGGER = STPLogger()
STATE = SenderState()

class SenderState(object):
    """ An object to keep track of state variables required for sending and
        processing STP segments.
    """
    def __init__(self):
        self.receiver_host_ip = ''
        self.receiver_port = 0
        self.file_name = ''
        self.data_file = None
        self.mws = 0
        self.mss = 0
        self.timeout = 0
        self.pdrop = 0.0
        self.seed = 0

def main(argv):
    """ Main function taking in commandline args. """
    # Retrieve data from command line input args.
    STATE.receiver_host_ip = argv[1]
    STATE.receiver_port = int(argv[2])
    STATE.file_name = argv[3]
    STATE.mws = int(argv[4])
    STATE.mss = int(argv[5])
    STATE.timeout = int(argv[6])
    STATE.pdrop = float(argv[7])
    STATE.seed = int(arg[8])

    # Open file for reading.
    STATE.data_file = open(STATE.file_name, 'r')



if __name__ == "__main__":
    main(sys.argv)

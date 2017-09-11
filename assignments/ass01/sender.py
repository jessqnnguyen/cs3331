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

def main(argv):
    """ Main function taking in commandline args. """
    # Retrieve server port from command line input args.
    port = int(argv[1])
    file_name = argv[2]

if __name__ == "__main__":
    main(sys.argv)

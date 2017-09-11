""" Segment related classes. """
from enum import Enum
from datetime import datetime
import string
import pickle

class FinState(Enum):
    """ States of connection termination. """
    FIN_WAIT_1 = 1
    FIN_WAIT_2 = 2
    TIME_WAIT = 3

class STPLogger(object):
    """ A helper logger class to assist with consistent printing of segment
        logging format.
    """
    def __init__(self):
        self.is_logging = True

    @classmethod
    def log(cls, log_type, time, segment_type, seq_num, bytes_num, ack_num):
        """ A helper function to obtain a log string in the format:
            <snd/rcv/drop> <time> <type of segment> <sequence number>
            <number of bytes> <ack number>

        Params:
            log_type: A string which can have the following values "snd",
                      "rcv" and "drop".
            time: A float containing the number of milliseconds which has
                  elapsed since the logger started.
            segment_type: A string containing information about what type of
                          segment it is which can have the following values:
                                * "S" (SYN)
                                * "A" (ACK)
                                * "F" (FIN)
                                * "D" (DATA)
            seq_num: An integer containing the sequence number of the segment.
            bytes_num: An integer containing the number of bytes of the data.
                       Note this field should only be set this value if
                       segment_type = "D".
            ack_num: An integer containing the acknowledgment number.
        """
        return (log_type.ljust(8) + str(time).ljust(10) +
                segment_type.ljust(5) + str(seq_num).ljust(10)
                + str(bytes_num).ljust(8) + str(ack_num).ljust(10))

    @classmethod
    def get_time_elapsed(cls, start_time):
        """ A helper function which returns time elapsed (ms) given a start
            time.

        Params:
            start_time: an datetime.datetime instance of the time to measure
                        elapsed time from.

        Returns: A float value which contains the ms elapsed since start_time.
        """
        return (datetime.now() - start_time).microseconds

class STPSegment(object):
    """ An STP segment which is used by a sender and receiver end point to
        transfer data reliably using the STP protocol.

    Attributes:
        source_ip: A string containing the source IP address of the segment.
        dest_ip: A string containing the destination IP address of the segment.
        source_port: An integer containing the source port of the segment.
        dest_port: An integer containing the destination port of the segment.
        seq_num: An integer containing the sequence number of the segment.
        ack_num: An integer containing the acknowledgement number of the
                 segment.
        data: A string containing the payload, optional.
        mss: An integer containing the maximum segment size in bytes.
        syn_flag: A boolean indicating whether the segment is requesting to
                  establish a STP connection, set to 1 if it is, optional.
        fin_flag: A boolean indicating whether the segment is requesting to
                  terminate a STP connection, set to 1 if it is, optional.
        rst_flag: A boolean indicating whether the segment is a notification
                  response that the previously received segment was addressed
                  to a port number that was not open, optional.
    """
    def __init__(self):
        """ Inits a basic STPSegment with all attributes set to 0, false
            or the empty string initially.

        Use set_address_attributes() to set address related attributes and
        set_seq_ack_num() to set attributes which store the sequence and
        acknowledgement number.
        """
        self.source_ip = 0
        self.dest_ip = 0
        self.source_port = 0
        self.dest_port = 0
        self.seq_num = 0
        self.ack_num = 0
        self.syn_flag = False
        self.fin_flag = False
        self.rst_flag = False
        self.data = ''
        self.mss = 0

    def set_address_attributes(self, source_ip, dest_ip, source_port,
                               dest_port):
        """ A help setter for address related attributes. """
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_port = source_port
        self.dest_port = dest_port

    def set_seq_ack_num(self, seq_num, ack_num):
        """ A helper setter to set attributes which store the sequence and
            acknowledgement numbers.
        """
        self.seq_num = seq_num
        self.ack_num = ack_num

    def send_segment(self, sock, addr):
        """ A helper function which wraps up a STPSegment and an
            address (An (IP, port) tuple) and sends it through the socket.
        """
        data = pickle.dumps(self)
        sock.sendto(data, addr)

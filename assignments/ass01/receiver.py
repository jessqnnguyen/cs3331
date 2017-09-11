""" Receiver operating on the STP Protocol module. """
import sys
# Socket programming library.
import socket
# Object serialization library.
import pickle
# System time library for logging.
from datetime import datetime
# Segment module.
from segment import STPSegment, STPLogger

LOG_FILE_NAME = "Receiver_log.txt"
STP_LOGGER = STPLogger()

class ReceiverState(object):
    """ An object to keep track of state variables required for processing
        STP segments.

    Attributes:
        receiver_port: An integer containing the port the receiver will be
                       receiving STP segments from.
        file_name: A string containing the name of the data file being
                  transferred.
        start_time: A datetime.datetime object storing the time the receiver
                    started listening on it's port.
        time_elapsed: A float containing the number of ms that has elapsed
                      since the receiver started listening on it's port. Used
                      for logging.
        curr_seq_num: An integer containing the current sequence number.
        sender_addr: An (IP, port #) tuple to keep track of the current sender
                     address.
        established_sender_addr: An (IP, port #) tuple to keep track of the
                                 sender address that has established a STP
                                 connection (via three way handshake).
        log_file: A file to write logs to. This file is initiated when this
                  object is initiated.
        data_received_num: An integer containing the number of bytes that the
                           receiver has received.
        segments_received_num: An integer containing the number of segments that
                               the receiver has received.
        duplicate_segments_received_num: An integer containing the number of
                                         duplicate segments received.
        is_connected: A bool to keep track of current connection state.
        is_connection_being_established: A bool to keep track of whether a
                                         three way handshake is occurring.
        is_connection_being_terminated: A bool to keep track of whether a
                                        connection is in the process of being
                                        terminated.
        data_file: Stores the file being written to. Intialise later after
                   connection has been established in:
                        process_connection_establishment_type_segment()
    """
    def __init__(self):
        """ Inits all attributes with 0 or False and opens a new file for the
            logger.
        """
        self.receiver_port = 0
        self.file_name = ''
        self.start_time = datetime.now()
        self.time_elapsed = 0
        self.curr_seq_num = 0
        self.curr_ack_num = 0
        self.sender_addr = 0
        self.established_sender_addr = 0
        self.log_file = open(LOG_FILE_NAME, "w")
        self.data_received_num = 0
        self.segments_received_num = 0
        self.duplicate_segments_received_num = 0
        self.is_connected = False
        self.is_connection_being_established = False
        self.is_connection_being_terminated = False
        self.is_file_transfer_complete = False
        self.data_file = None

def main(argv):
    """ Main function taking in commandline args. """
    # Retrieve server port from command line input args.
    port = int(argv[1])
    file_name = argv[2]

    # Store max buffer size.
    max_buffer_size = 1024

    # Create a UDP socket instance using IPv4 addresses (AF_INET) and
    # UDP protocol (SOCK_DGRAM).
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind it to the input receiver port.
    sock.bind((socket.gethostname(), port))

    states = ReceiverState()
    states.receiver_port = port
    states.file_name = file_name

    while not states.is_file_transfer_complete:
        print("Waiting to receive from port %d" % port)
        data = sock.recv(max_buffer_size)
        if data:
            states.segments_received_num += 1

            # Deserialize segment back into an STPSegment object.
            segment = pickle.load(data)

            # Initialise a basic STP segment reply object with address params
            # (source_ip, dest_ip, source_port, dest_port) and mss field set.
            segment_reply = init_segment_reply(segment, states)

            # Store sender address extracted from segment source IP and port
            # fields.
            states.sender_addr = (segment.source_ip, segment.source_port)
            # Connection not yet established case.
            if not states.is_connected:
                if segment.syn_flag:
                    process_connection_establishment(sock, segment,
                                                     segment_reply, states)
            # Connection established case.
            elif states.sender_addr == states.established_sender_addr:
                # Check if the segment is requesting a connection termination.
                if segment.fin_flag:
                    process_connection_termination(sock, segment, segment_reply,
                                                   states)
                # Process a data type segment.
                else:
                    process_data_type_segment(sock, segment, segment_reply,
                                              states)
    states.log_file.write("Amount of data received (bytes): %d"
                          % states.data_received_num)
    states.log_file.write("# data segments received: %d"
                          % states.segments_received_num)
    states.log_file.write("# duplicate segments received: %d"
                          % states.duplicate_segments_received_num)
    states.log_file.close()

def process_connection_establishment(sock, segment, segment_reply, states):
    """ A helper function to process segments with the syn_flag set. """
    update_time_elapsed(states)
    states.log_file.write(STP_LOGGER.log("rcv", states.time_elapsed, "S",
                                         segment.seq_num, segment.mss,
                                         segment.ack_num))
    # If segment is the first stage of three way handshake.
    if not states.is_connection_being_established:
        states.is_connection_being_established = True
        segment_reply.syn_flag = True
        states.curr_ack_num = segment.seq_num + 1
        segment_reply.set_seq_ack_num(states.curr_seq_num, states.curr_ack_num)
        segment_reply.send_segment(sock, states.sender_addr)
        states.log_file.write(STP_LOGGER.log(states.log_file, "snd",
                                             states.time_elapsed, "S",
                                             segment_reply.seq_num,
                                             segment_reply.mss,
                                             segment_reply.ack_num))
        states.curr_seq_num += 1
        states.established_sender_addr = states.sender_addr
    # If the segment is the final stage of three way
    # handshake.
    is_final_stage_of_handshake = ((states.is_connection_being_established) and
                                   (segment.ack_num == states.curr_seq_num + 1)
                                   and (states.sender_addr !=
                                        states.established_sender_addr))
    if is_final_stage_of_handshake:
        states.is_connected = True
        states.data_file = open(states.file_name, "w")
        states.is_connection_being_established = False
        states.curr_ack_num += 1

def process_connection_termination(sock, segment, segment_reply, states):
    """ A helper function to process segments with the fin_flag set. """
    update_time_elapsed(states)
    states.log_file.write(STP_LOGGER.log(states.log_file, "rcv",
                                         states.time_elapsed, "F",
                                         segment.seq_num, segment.mss,
                                         segment.ack_num))
    if not states.is_connection_being_terminated:
        states.is_connection_being_terminated = True
        # First send a segment reply with an ACK.
        states.curr_ack_num += 1
        segment_reply.set_seq_ack_num(states.curr_seq_num, states.curr_ack_num)
        segment_reply.fin_flag = True
        segment_reply.send_segment(sock, states.sender_addr)
        update_time_elapsed(states)
        states.log_file.write(STP_LOGGER.log(states.log_file, "snd",
                                             states.time_elapsed, "FA",
                                             segment_reply.seq_num,
                                             segment_reply.mss,
                                             segment_reply.ack_num))
        # TODO: Remove this commented out section once clarified
        # whether connection termination requires two segments?
        # Then send a segment reply with the FIN flag set.
        # segment_reply.fin_flag(True)
        # segment_reply.send_segment(sock, SENDER_ADDR)
        # STP_LOGGER.log(states.log_file, "snd", states.time_elapsed, "F"
        #               segment_reply.seq_num, segment_reply.mss,
        #               segment.ack_num)
    else:
        # Check for final reply ACK to terminate connection.
        if segment.ack_num == states.curr_seq_num + 1:
            states.is_connected = False
            states.is_connection_being_terminated = False
            states.data_file.close()
            states.is_file_transfer_complete = True

def process_data_type_segment(sock, segment, segment_reply, states):
    """ A helper function to process segments where the connection
        has been established which contain a data payload.
    """
    # Check segment is a duplicate, that is the sequence
    # number is equal to the most recent acknowledged byte
    # minus 1.
    update_time_elapsed(states)
    states.log_file.write(STP_LOGGER.log(states.log_file, "rcv",
                                         states.time_elapsed, "D",
                                         segment.seq_num,
                                         segment.mss, segment.ack_num))
    if segment.seq_num == states.curr_ack_num - 1:
        states.duplicate_segments_received_num += 1
    else:
        states.data_file.write(segment.data)
        states.curr_ack_num += segment.mss
        states.curr_seq_num += 1
        # Update logger vars.
        states.data_received_num += segment.mss
        states.segments_received_num += 1
    segment_reply.set_seq_ack_num(states.curr_seq_num, states.curr_ack_num)
    segment_reply.send_segment(sock, states.sender_addr)
    update_time_elapsed(states)
    states.log_file.write(STP_LOGGER.log(states.log_file, "snd",
                                         states.time_elapsed, "A",
                                         segment_reply.seq_num,
                                         segment_reply.mss,
                                         segment_reply.ack_num))

def init_segment_reply(segment, states):
    """ Helper function to initialise a basic STPSegment reply with address
        params set and also mss set.

        Segments sent from the receiver should always have the mss=0
        since only segments of type "D" do not get sent from this end.
    """
    segment_reply = STPSegment()
    segment_reply.mss = 0
    # TODO: Change this to a call to the socket's host name func.
    # set_address_attributes(source_ip, dest_ip, source_port,
    #                        dest_port)
    segment_reply.set_address_attributes("localhost",
                                         segment.source_ip,
                                         states.receiver_port,
                                         segment.source_port)
    return segment_reply

def update_time_elapsed(states):
    """ A helper function to assist with logging to recalculate and set
        the time elapsed.
    """
    states.time_elapsed = states.log_file.write(STP_LOGGER.
                                                get_time_elapsed
                                                (states.start_time))

if __name__ == "__main__":
    main(sys.argv)

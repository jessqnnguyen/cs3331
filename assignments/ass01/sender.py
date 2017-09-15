# Jessica Nguyen
# z5018882
# CS3331 Assignment 1
# python3

""" Sender operating on the STP Protocol module. """
import sys
# Socket programming library.
import socket
# Object serialization library.
import pickle
# System time library for logging.
from datetime import datetime
# System library to obtain file size.
import os
# System library for random number generation for PLD.
import random
# Timer class
from threading import Timer, Lock, Thread
import threading
import time

# Segment module.
from segment import STPSegment, STPLogger, FinState

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
        self.timeout = 0.0
        self.pdrop = 0.0
        self.seed = 0
        self.remainder_segment_size = 0
        self.receiver_addr = None
        self.send_base = 0
        self.next_seq_num = 0
        self.ack_num = 0
        self.data_segments = {} # A dictionary of (sequence number, data) pairs.
        self.is_timer_running = False
        self.log_file = open(LOG_FILE_NAME, "w")
        self.data_transferred_num = 0
        self.data_segments_sent_num = 0
        self.retransmitted_segments_num = 0
        self.duplicate_acks_received_num = 0
        self.is_file_transfer_complete = False
        self.last_seq_num = -1
        self.is_connection_being_terminated = False
        self.is_connected = False
        self.is_connection_being_established = False
        self.curr_fin_state = FinState.NOT_TERMINATING
        self.time_elapsed = 0.0
        self.start_time = None
        self.unacknowledged_bytes_num = 0
        self.sock = None
        self.ack_received_before_timeout_event = threading.Event()
        self.lock = Lock()
        self.file_transfer_complete_event = threading.Event()
        self.received_acks = {}
        self.dropped_packets_num = 0

LOG_FILE_NAME = "Sender_log.txt"
STP_LOGGER = STPLogger()
STATE = SenderState()
MAX_BUFFER_SIZE = 4096

def main(argv):
    """ Main function taking in commandline args. """
    # Retrieve data from command line input args.
    STATE.receiver_host_ip = argv[1]
    STATE.receiver_port = int(argv[2])
    STATE.file_name = argv[3]
    STATE.mws = int(argv[4])
    STATE.mss = int(argv[5])
    STATE.timeout = float(argv[6]) / 1000 # Convert to s from ms
    STATE.pdrop = float(argv[7])
    STATE.seed = int(argv[8])

    # Init random number generator with seed number.
    random.seed(STATE.seed)

    if STATE.receiver_port != 2500:
        STATE.sender_port = 2500
    else:
        STATE.sender_port = 3000

    STATE.sender_ip = socket.gethostbyname(socket.gethostname())

    if STATE.sender_ip == STATE.receiver_host_ip or STATE.receiver_host_ip == '127.0.0.1':
        STATE.receiver_addr = ('localhost', STATE.receiver_port)
        STATE.sender_ip = 'localhost'
    else:
        STATE.receiver_addr = (STATE.receiver_host_ip, STATE.receiver_port)

    # Init send base and next sequence number to 0 initially.
    # This is mostly redundant as it's alredy set in the constructor
    # as a default value.
    STATE.send_base = 0
    STATE.next_seq_num = 0

    # Open file for reading.
    STATE.data_file = open(STATE.file_name, 'r')

    # Create a UDP socket instance using IPv4 addresses (AF_INET) and
    # UDP protocol (SOCK_DGRAM).
    try:
        STATE.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        STATE.sock.bind((STATE.sender_ip, STATE.sender_port))
        STATE.start_time = datetime.now()
    except socket.error:
        print("Failed to complete socket.")
        sys.exit()

    while not STATE.is_file_transfer_complete:
        # print("is state connected = %s" % str(STATE.is_connected))
        if not STATE.is_connected:
            if not STATE.is_connection_being_established:
                start_three_way_hand_shake(STATE.sock)
            data, receiver_addr = STATE.sock.recvfrom(MAX_BUFFER_SIZE)
            if data:
                segment = pickle.loads(data)
                if segment.syn_flag and segment.ack_flag:
                    STATE.send_base += segment.ack_num
                    if segment.ack_num == STATE.next_seq_num:
                        complete_three_way_hand_shake(STATE.sock, segment)
        else:
            STATE.unacknowledged_bytes_num = STATE.next_seq_num - STATE.send_base
            # Only send data when the the total number of unacknowledged bytes
            # is less than the maximum window size and the data transfer is not
            # yet complete (i.e !(next_seq_num > last_seq_num))
            while STATE.unacknowledged_bytes_num < STATE.mws and STATE.next_seq_num <= STATE.last_seq_num:
                transmit_next_data_segment(STATE.sock)
                check_for_incoming_segments(STATE.sock)

            STATE.unacknowledged_bytes_num = STATE.next_seq_num - STATE.send_base

        if STATE.next_seq_num > STATE.last_seq_num and STATE.last_seq_num != -1:
            if not STATE.is_connection_being_terminated:
                start_connection_termination(STATE.sock)

    while STATE.is_connected:
        data = STATE.sock.recv(1024)
        complete_connection_termination(data)

    STATE.sock.close()
    STATE.log_file.write("\nAmount of data transferred (bytes): %d \n"
                          % STATE.data_transferred_num)
    STATE.log_file.write("Number of data segments sent: %d \n"
                          % STATE.data_segments_sent_num)
    STATE.log_file.write("Number of packets dropped by the PLD module: %d \n"
                          % STATE.dropped_packets_num)
    STATE.log_file.write("Number of retransmitted segments sent: %d \n"
                          % STATE.retransmitted_segments_num)
    STATE.log_file.write("Number of duplicate acks received: %d \n"
                          % STATE.duplicate_acks_received_num)
    STATE.log_file.close()

def is_packet_dropped():
    is_packet_dropped = True
    x = random.random()

    if x > STATE.pdrop:
        is_packet_dropped = False

    return is_packet_dropped

def complete_connection_termination(data):
    if data:
        segment = pickle.loads(data)
        if segment.ack_flag:
            if segment.ack_num in STATE.received_acks.keys():
                print("duplicate ack detected")
                STATE.duplicate_acks_received_num += 1
            else:
                STATE.curr_fin_state = FinState.FIN_WAIT_2

            update_time_elapsed()
            STATE.log_file.write(STP_LOGGER.log("rcv", STATE.time_elapsed,
                                                "A", segment.seq_num,
                                                len(segment.data),
                                                segment.ack_num))

        elif segment.fin_flag and STATE.curr_fin_state == FinState.FIN_WAIT_2:
            update_time_elapsed()
            STATE.log_file.write(STP_LOGGER.log("rcv", STATE.time_elapsed,
                                                "F", segment.seq_num,
                                                len(segment.data),
                                                segment.ack_num))
            ack_segment = init_basic_stp_segment()
            ack_segment.set_seq_ack_num(STATE.next_seq_num, segment.seq_num + 1)
            ack_segment.ack_flag = True
            ack_segment.send_segment(STATE.sock, STATE.receiver_addr)
            update_time_elapsed()
            STATE.log_file.write(STP_LOGGER.log("snd", STATE.time_elapsed,
                                                "A", ack_segment.seq_num,
                                                len(ack_segment.data),
                                                ack_segment.ack_num))
            STATE.curr_fin_state = FinState.TIME_WAIT
            STATE.is_connected = False
            STATE.data_file.close()
            STATE.is_connection_being_terminated = False
            STATE.curr_fin_state = FinState.NOT_TERMINATING

def transmit_next_data_segment(sock):
    if not STATE.is_timer_running:
        start_timer()
        STATE.is_timer_running = True

    if STATE.next_seq_num == STATE.last_seq_num:
        return

    data_segment = create_next_data_segment()
    data_size = len(data_segment.data)

    if not is_packet_dropped():
        data_segment.send_segment(sock, STATE.receiver_addr)
        update_time_elapsed()
        STATE.log_file.write(STP_LOGGER.log("snd",
                                             STATE.time_elapsed, "D",
                                             data_segment.seq_num,
                                             data_size,
                                             data_segment.ack_num))
        STATE.data_transferred_num += data_size
    else:
        STATE.dropped_packets_num += 1
        update_time_elapsed()
        STATE.log_file.write(STP_LOGGER.log("drop",
                                          STATE.time_elapsed, "D",
                                         data_segment.seq_num,
                                         data_size,
                                         data_segment.ack_num))
    STATE.data_segments_sent_num += 1
    STATE.next_seq_num += data_size
    print("updating next_seq_num from %d to %d" % (STATE.next_seq_num - data_size, STATE.next_seq_num))
    start_timer()

def check_for_incoming_segments(sock):
    data, receiver_addr = sock.recvfrom(MAX_BUFFER_SIZE)
    if data:
        # Extract the ack number.
        segment = pickle.loads(data)
        update_time_elapsed()
        STATE.log_file.write(STP_LOGGER.log("rcv",
                                             STATE.time_elapsed, "A",
                                             segment.seq_num,
                                             len(segment.data),
                                             segment.ack_num))
        if segment.ack_flag:
            STATE.ack_num = segment.seq_num
            # Data transfer complete - receiver sends ack number of
            # last seq num.
            if segment.ack_num == STATE.last_seq_num:
                start_connection_termination(STATE.sock)

            #  Duplicate ack case.
            elif segment.ack_num in STATE.received_acks.keys():
                print("duplicate ack detected")
                STATE.duplicate_acks_received_num += 1
                # Fast retransmit if ack received 3 times previously.
                if STATE.received_acks[segment.ack_num] == 3:
                    print("fast retransmit case registered")
                    data_segment = init_basic_stp_segment()
                    data_segment.set_seq_ack_num(segment.ack_num, STATE.ack_num)
                    try:
                        data_segment.data = STATE.data_segments[STATE.ack_num]
                    except KeyError:
                        print("Key error on %s" % STATE.ack_num)
                        print("Dictionary has keys: %s" % str(STATE.data_segments.keys()))

                    data_segment.send_segment(STATE.sock, STATE.receiver_addr)
                    STATE.retransmitted_segments_num += 1
                    update_time_elapsed()
                    STATE.log_file.write(STP_LOGGER.log("snd",
                                                         STATE.time_elapsed, "D",
                                                         data_segment.seq_num,
                                                         len(data_segment.data),
                                                         data_segment.ack_num))
            elif segment.ack_num > STATE.send_base:
                print("Send base updated from %d to %d" % (STATE.send_base, segment.ack_num))
                print("next_seq_num = %d" % (STATE.next_seq_num))
                STATE.send_base = segment.ack_num
                STATE.ack_received_before_timeout_event.set()
                # Start timer again if there are still any unacknowledged bytes.
                if (STATE.next_seq_num > STATE.send_base):
                    start_timer()

            if not(segment.ack_num in STATE.received_acks.keys()):
                STATE.received_acks[segment.ack_num] = 1
            else:
                STATE.received_acks[segment.ack_num] += 1

def start_connection_termination(sock):
    fin_segment = init_basic_stp_segment()
    seq_num = STATE.next_seq_num
    ack_num = STATE.ack_num
    fin_segment.set_seq_ack_num(seq_num, ack_num)
    fin_segment.fin_flag = True
    fin_segment.send_segment(sock, STATE.receiver_addr)
    update_time_elapsed()
    STATE.log_file.write(STP_LOGGER.log("snd",
                                         STATE.time_elapsed, "F",
                                         fin_segment.seq_num,
                                         len(fin_segment.data),
                                         fin_segment.ack_num))
    STATE.is_connection_being_terminated = True
    STATE.is_file_transfer_complete = True
    STATE.file_transfer_complete_event.set()
    STATE.next_seq_num += 1
    STATE.curr_fin_state = FinState.FIN_WAIT_1

def complete_three_way_hand_shake(sock, syn_ack_segment):
    update_time_elapsed()
    STATE.log_file.write(STP_LOGGER.log("rcv", STATE.time_elapsed,
                                        "SA", syn_ack_segment.seq_num,
                                        len(syn_ack_segment.data),
                                        syn_ack_segment.ack_num))
    syn_segment = init_basic_stp_segment()
    seq_num = STATE.next_seq_num
    ack_num = syn_ack_segment.seq_num + 1
    STATE.ack_num = ack_num
    syn_segment.set_seq_ack_num(seq_num, ack_num)
    syn_segment.ack_flag = True
    syn_segment.syn_flag = True
    syn_segment.send_segment(sock, STATE.receiver_addr)
    update_time_elapsed()
    STATE.log_file.write(STP_LOGGER.log("snd",
                                         STATE.time_elapsed, "S",
                                         syn_segment.seq_num,
                                         len(syn_segment.data),
                                         syn_segment.ack_num))
    STATE.is_connection_being_established = False
    STATE.is_connected = True
    STATE.next_seq_num += 1
    compute_segment_sizes()
    STATE.is_timer_running = True
    print("Dictionary has keys: %s" % str(STATE.data_segments.keys()))

def start_three_way_hand_shake(sock):
    syn_segment = init_basic_stp_segment()
    seq_num = STATE.next_seq_num
    ack_num = STATE.ack_num
    syn_segment.set_seq_ack_num(seq_num, ack_num)
    syn_segment.syn_flag = True
    syn_segment.send_segment(sock, STATE.receiver_addr)
    update_time_elapsed()
    data_size = len(syn_segment.data)
    update_time_elapsed()
    STATE.log_file.write(STP_LOGGER.log("snd", STATE.time_elapsed, "S",
                         syn_segment.seq_num, data_size, syn_segment.ack_num))
    STATE.is_connection_being_established = True
    STATE.next_seq_num += 1

def init_basic_stp_segment():
    data_segment = STPSegment()
    data_segment.mss = STATE.mss
    # host_name = socket.gethostbyname(socket.gethostname())
    if (STATE.sender_ip == STATE.receiver_host_ip or STATE.receiver_host_ip == '127.0.0.1'):
        # print("this ran")
        data_segment.set_address_attributes('localhost',
                                            'localhost',
                                            STATE.sender_port,
                                            STATE.receiver_port)
    else:
        data_segment.set_address_attributes(STATE.sender_ip,
                                            STATE.receiver_host_ip,
                                            STATE.sender_port,
                                            STATE.receiver_port)
    return data_segment

def create_next_data_segment():
    data_segment = init_basic_stp_segment()
    seq_num = STATE.next_seq_num
    ack_num = STATE.ack_num
    data_segment.set_seq_ack_num(seq_num, ack_num)
    if not STATE.data_segments:
        print("dict is empty!")
    try:
        data_segment.data = STATE.data_segments[seq_num]
    except KeyError:
        print("Key error on %s" % seq_num)
        print("Dictionary has keys: %s" % str(STATE.data_segments.keys()))
    return data_segment



def start_timer():
    print("timer started")
    STATE.ack_received_before_timeout_event.clear()
    timer_thread = Thread(target=wait_for_timeout_event)
    timer_thread.daemon = True
    timer_thread.start()
    timer_thread.join(timeout=STATE.timeout)
    print("timed out")
    if not STATE.ack_received_before_timeout_event.is_set():
        process_timeout_event()
    if timer_thread.is_alive():
        print("thread is still alive")
    else:
        print("thread completed")


def wait_for_timeout_event():
    while True:
        time.sleep(0.1) # Sleep 100 ms.
        if STATE.ack_received_before_timeout_event.is_set() or STATE.file_transfer_complete_event.is_set():
            break

def process_timeout_event():
    """ A helper function which processes a timeout event.

    This function is passed into a Timer call.
    """
    STATE.lock.acquire()
    # Retransmit sequence with oldest unacknowledged sequence number.
    try:
        data_segment = init_basic_stp_segment()
        data_segment.set_seq_ack_num(STATE.send_base, STATE.ack_num)
        try:
            data_segment.data = STATE.data_segments[STATE.send_base]
        except KeyError:
            print("Key error on %s" % STATE.send_base)
            print("Dictionary has keys: %s" % str(STATE.data_segments.keys()))

        data_segment.send_segment(STATE.sock, STATE.receiver_addr)
        print("just sent segment with seq %d and ack %d" % (data_segment.seq_num, data_segment.ack_num))
        update_time_elapsed()
        STATE.log_file.write(STP_LOGGER.log("snd",
                                             STATE.time_elapsed, "D",
                                             data_segment.seq_num,
                                             len(data_segment.data),
                                             data_segment.ack_num))
        STATE.retransmitted_segments_num += 1
    finally:
        STATE.lock.release()

def compute_segment_sizes():
    # Break up data file into segments of MSS.
    file_size = os.path.getsize(STATE.file_name)
    if file_size == 0:
        print ("File error: file can not be empty!")
        sys.exit()
    next_seq_num = STATE.next_seq_num
    STATE.send_base = next_seq_num
    if (file_size %  STATE.mss != 0):
        # x = qb + r
        # file_size = max_segment_size + (file_size % STATE.mss)
        # max_segment_size = file_size - (file_size % STATE.mss)
        STATE.remainder_segment_size = file_size % STATE.mss
        nearest_mss_multiple = file_size - STATE.remainder_segment_size
        for i in range(next_seq_num, next_seq_num + nearest_mss_multiple, STATE.mss):
            read_write_data(i, STATE.mss)
            next_seq_num += STATE.mss
        read_write_data(next_seq_num, STATE.remainder_segment_size)
        STATE.last_seq_num = next_seq_num + STATE.remainder_segment_size
    else:
        for i in range(next_seq_num, next_seq_num + file_size, STATE.mss):
            read_write_data(i, STATE.mss)
            next_seq_num += STATE.mss
            STATE.last_seq_num = next_seq_num + STATE.mss
    print("last seq num = %d" % STATE.last_seq_num)

def read_write_data(seq_num, bytes_num):
    data = STATE.data_file.read(bytes_num)
    print ("adding data_segments[%d] = %s" % (seq_num, data))
    STATE.data_segments[seq_num] = data

def update_time_elapsed():
    """ A helper function to assist with logging to recalculate and set
        the time elapsed.
    """
    time_delta = ((datetime.now() - STATE.start_time).microseconds)/1000
    # STATE.time_elapsed = STP_LOGGER.get_time_elapsed(STATE.start_time)
    STATE.time_elapsed = time_delta


if __name__ == "__main__":
    sys.stdout = sys.stderr
    main(sys.argv)

# CS3331 Lab 4: Exploring TCP 

## Exercise 1: Understanding TCP using Wireshark

### Question 1

The IP address and TCP port number of the client computer is `192.168.1.102` and `1161` respectively.

### Question 2

The IP address of `gaia.cs.umass.edu` is `128.119.245.12` and it is receiving TCP segments on port `80`.

### Question 3

The sequence number of the TCP SYN segment that is used to initiate the TCP connection between the client computer and `gaia.cs.umass.edu` is 0. The SYN bit is set in the flag field of the segment which identifies the segment as a SYN segment.

### Question 4

The sequence number of the SYNACK segment sent by `gaia.cs.umass.edu` to the client computer in reply to the SYN the client computer sent, is 0 and the acknowledgment number is 1. `gaia.cs.umass.edu` determined this value based on the fact that it is the first SYN segment's sequence number (0) plus 1. The bits for SYN and ACK are set in the flags field of this segment which identify it as a SYNACK segment.

### Question 5

The sequence number of the ACK segment sent by the client computer in response to the SYNACK is 1 and the acknowledgment number is 1.  This segment does not contain any data and this segment is identified as an ACK segment because the ACK flag is set in the flags field of the segment.

### Question 6

The sequence number of the TCP segment containing the HTTP POST command is 1.

### Question 7

Tabular data for the first 6 TCP data segments sent from the client to the `gaia.cs.umass.edu`. Estimated RTT values are calculated using an alpha value of 0.125 hence (1- 0.125) = 0.875.

Sequence # | Segment data size (bytes) | Time sent       | Time ACK received | rtt (ms) | estimated rtt
---------- | ------------------------- | --------------- | ----------------- | -------- | -------------
1          | 565			            | 23:44:20.59685  | 23:44:20.624318   | 27.468   | 27.468
566        | 1460                      | 23:44:20.612118 | 23:44:20.647675   | 35.557   | (0.875)(27.468) + 35.557 = 59.5915
2026       | 1460                      | 23:44:20.624407 | 23:44:20.694466   | 70.059   | (0.875)(59.5915) + 70.059 = 122.2015625
3486       | 1460 					    | 23:44:20.625071 | 23:44:20.694466   | 69.395   | (0.875)(122.2015625) + 69.395 = 176.321367187       
4946       | 1460                      | 23:44:20.647786 | 23:44:20.739499   | 91.713   | (0.875)(176.321367187) + 91.713 = 245.994196289
6406       | 1460                      | 23:44:20.648538 | 23:44:20.78768    | 139.142  | (0.875)(245.994196289) + 139.142 = 354.386921753

### Question 8 

The length of each of the first six TCP segments is 619, 1514, 1514, 1514, 1514, 1514 bytes.

### Question 9 

The minimum amount of available buffer space advertised at the receiver for the entire trace is 5840 bytes. 

[ ] Answer the following question: Does the lack of receiver buffer space ever throttle the sender?

### Question 10

Yes there is one at segment number 9, an ACK sent from `gaia.cs.umass.edu` to the client. I applied the filter `tcp.analysis.retransmission` on Wireshark to find the retransmitted segment.

### Question 11

How much data does the receiver typically acknowledge in an ACK? Can you identify cases where the receiver is ACKing every other received segment (recall the discussion about delayed acks from the Week 5 lecture notes or Section 3.5 of the text).

### Question 12

What is the throughput (bytes transferred per unit time) for the TCP connection? Explain how you calculated this value. 


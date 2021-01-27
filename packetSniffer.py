import socket as sk
from struct import *
import sys
import os

def extact_ethernet_head(data):    
    dest, src, prototype = unpack('! 6s 6s H', data[:14])
    dest_mac = format_ethernet_mac(dest)
    src_mac = format_ethernet_mac(src)
    proto = sk.htons(prototype)
    data = data[14:]
    return dest_mac, src_mac, proto, data 

def format_ethernet_mac(address):
    strings = map('{:02x}'.format, address)
    strings = ':'.join(strings).upper()
    return strings

def get_mac_addr(address):
 return '.'.join(map(str, address))

def ipv4_header(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 0xF) * 4
    ttl, proto, src, target = unpack('!8xBB2x4s4s', data[:20])
    src = get_mac_addr(src)
    target = get_mac_addr(target)
    data = data[header_length:]
    return version, header_length, ttl, proto, src, target, data

def tcp_unpack(data):
    tcpheader = unpack('!HHLLH' , data[:14]) 
    source_port = tcpheader[0]
    dest_port = tcpheader[1]
    sequence = tcpheader[2]
    acknowledgement = tcpheader[3]
    off_reserved = tcpheader[4]
    tcph_length = (off_reserved >> 12) * 4
    data = data[tcph_length:]
    return source_port, dest_port, sequence, acknowledgement, data

def icmp_unpack(data):
    icmpheader = unpack('!BBH' , data[:4]) 
    Type = icmpheader[0]
    Code = icmpheader[1]
    Checksum = icmpheader[2]
    return Type, Code, Checksum, data[4:]
        
def udp_unpack(data):
    source_port, dest_port, length  = unpack('!HH2xH' , data[:8]) 
    return source_port, dest_port, length, data[8:]

def main():
    # creating a raw socket with AF_PACKET family raw socket 

    inet_socket = sk.socket(sk.AF_PACKET, sk.SOCK_RAW, sk.ntohs(0x0003))

    # run infinite loop to receive data from the socket:
    i = 0
    while True:
        try:
            raw_data, address = inet_socket.recvfrom(65535)
            eth = extact_ethernet_head(raw_data)
            print('\nEthernet Frame:')
            print('Destination: {}, Source: {}, Protocol: {}'.format(eth[0], eth[1],
            eth[2]))
            # get IP version 4 for normal internet
            if eth[2] == 8:
                ipv4 = ipv4_header(eth[3])
                print( '\t - ' + 'IPv4 Packet:')
                print('\t\t - ' + 'Version: {}, Header Length: {}, TTL:{},'.format(ipv4[0], ipv4[1], ipv4[2]))
                print('\t\t - ' + 'Protocol: {}, Source: {}, Target:{}'.format(ipv4[3], ipv4[4], ipv4[5]))
            
                if ipv4[3] == 6:
                    tcps = tcp_unpack(ipv4[6]) 
                    print('\t\t - ' + 'TCP Protocal:')
                    print('\t\t\t - ' + 'Source Port: {}, Destination Port: {}'.format(tcps[0], tcps[1]))
                    print('\t\t\t - ' + 'Sequence: {}, Acknowledgment: {}'.format(tcps[2], tcps[3])) 
                            
                elif ipv4[3] == 1:
                    icmps = icmp_unpack(ipv4[6])
                    print('\t\t - ' + 'ICMP Protocal:')
                    print('\t\t\t - ' + 'Type: {}, Code: {}, Checksum:{},'.format(icmps[0], icmps[1],icmps[2])) 
            
                elif ipv4[3] == 17:
                    udps = udp_unpack(ipv4[6])
                    print('\t\t - ' + 'UDP Protocal:')
                    print('\t\t\t - ' + 'Source Port: {}, Destination Port: {}, Length: {}'.format(udps[0], udps[1], udps[2]))
                else:
                    print('Other protocal')
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


if __name__=='__main__':
    main()



















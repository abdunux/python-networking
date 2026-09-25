import socket
import os # to detect the system's name

#HOST ip address to listen on 
HOST = '192.168.1.203'


def main():
    #create a raw socket (we recieve packets with their headers (ip, tcp ...)) and bind it to the local interface
    if os.name == 'nt':
        #the protocol to capture : give me ALL IP packets (no filter)
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))

    # Include the IP header in captured packets : ip headre include = 1
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Enable promiscuous mode on Windows
    #the card accepts ALL packets passing through the network segment
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    #capture one packet : 65565 max size of an ip packet
    print(sniffer.recvfrom(65565))

    # Disable promiscuous mode on Windows
    if os.name == 'nt':
        sniffer.ioctl(
            socket.SIO_RCVALL,
            socket.RCVALL_OFF
        )

if __name__ == '__main__':
    main()


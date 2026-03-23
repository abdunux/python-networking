######## UDP CLIENT

import socket

target_host_2 = "127.0.0.1"
target_port_2 = 9997

client_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_2.sendto(b"hello are you there", (target_host_2, target_port_2)) # b = bytes

data, addr = client_2.recvfrom(4096) # 4096 taille max en octets

print(data.decode())
client_2.close()

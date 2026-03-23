import socket

# TCP CLIENT
target_host = "127.0.0.1"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

client.send(b"bonjour serveur !! ")
# receive some data
response = client.recv(4096)
print("[CLIENT] Reponse :", response.decode())
client.close()


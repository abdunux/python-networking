# crée un serveur SSH
# attend qu’un client se connecte
# authentifie avec username/password
# envoie des commandes au client
# reçoit les résultats

# serveur de contrôle
import socket
import paramiko
import threading
import sys

# charge une clé privée RSA
HOST_KEY = paramiko.RSAKey(filename='test_rsa.key')

# creer ssh server
class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    # Autorise uniquement : les connexions de type session
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == "user") and (password == "password"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


def start_server(server_ip, port):
    try:
        # Création du serveur TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Permet de réutiliser le port rapidement
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server_ip, port))
        sock.listen(5)
        print(f"[+] Listening on {server_ip}:{port}")

        client, addr = sock.accept()
        print(f"[+] Connection from {addr}")

    except Exception as e:
        print(f"[-] Listen failed: {e}")
        sys.exit(1)

    # Transformation en serveur SSH
    try:
        # Convertit la connexion TCP en connexion SSH
        transport = paramiko.Transport(client)
        # Donne l’identité du serveur
        transport.add_server_key(HOST_KEY)
        
        #Lancement du serveur SSH
        server = Server()
        transport.start_server(server=server)

        # Attend que le client ouvre un canal (max 20 sec)
        chan = transport.accept(20)

        if chan is None:
            print("[-] No channel")
            sys.exit(1)

        print("[+] Authenticated!")

        # recevoir le message initial
        print(chan.recv(1024).decode())

        # boucle de Controle
        while True:
            command = input("Enter command: ")

            if command != "exit":
                chan.send(command)
                response = chan.recv(8192)
                print(response.decode())
            else:
                chan.send("exit")
                print("Exiting...")
                transport.close()
                break

    except Exception as e:
        print(f"[-] Exception: {e}")
        transport.close()


if __name__ == '__main__':
    server_ip = "0.0.0.0"
    port = 2222

    start_server(server_ip, port)
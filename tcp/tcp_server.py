import socket
import threading

IP = '0.0.0.0'  # ecoute sur toutes les interfaces
PORT = 9999


def main():
    # creer un socket tcp
    # Donc tu demandes a lOS : Cree-moi un socket pour recevoir des connexions TCP avec IPv4.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 1 attacher le socket a une adresse et un port.
    server.bind((IP, PORT))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # apres bind
    #Sans ça, si tu arrêtes et relances le serveur rapidement, tu auras `OSError: Address already in use`.
    #
    # 2 Accepter maximum 5 connexions en attente avant de refuser les suivantes.
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')
    print(f"[SERVEUR] En ecoute sur {IP}:{PORT}")

    while True:
        # 3 accept() : cree une NOUVELLE socket : Cette socket est speciale pour ce client (est distincte de la socket principale)
                    #   Bbbloque le serveur jusqua ce qu un client se connecte
                    #   Le serveur attend qu un client fasse connect()
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')

        client_handler = threading.Thread(
            target=handle_client,
            args=(client,)
        )
        client_handler.start()               # 4


# def handle_client(client_socket):            # 5
#     with client_socket as sock:
#         while True:                          #  reste en vie
#             request = sock.recv(1024)
#             if not request:                  # client déconnecté
#                 break
#             print(f'[*] Received: {request.decode("utf-8")}')
#             sock.send(b'ACK recu aa')

def handle_client(client_socket):            
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK recu aa')


if __name__ == '__main__':
    main()

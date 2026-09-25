import socket
import argparse
# client TCP interactif

parser = argparse.ArgumentParser(description="Client TCP interactif")
parser.add_argument("-t", "--target", type=str, required=True, help="Adresse IP ou hostname du serveur")
parser.add_argument("-p", "--port", type=int, required=True, help="Port du serveur")
args = parser.parse_args()

target_host = args.target
target_port = args.port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
print("[CLIENT] Connecté au serveur. Tapez vos messages:")

try:
    while True:
        message = input("> ")  # lire depuis le terminal
        if message.lower() in ("exit", "quit"):  # pour fermer proprement
            print("[CLIENT] Déconnexion...")
            break
        client.send(message.encode())  # envoyer au serveur
        response = client.recv(4096)  # recevoir la réponse
        print("[SERVEUR]", response.decode())
finally:
    client.close()

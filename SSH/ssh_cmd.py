

#ce fichier est un simple client qui se connecte à un serveur SSH et exécuter UNE commande
#### EQUINALENT A ### ssh user@ip "commande"

# ssh_cmd.py utilise Paramiko pour :
#  se connecter à un vvvvvvvvvvvvrai serveur SSH
#  exécuter UNE commande
# afficher le résultat

import paramiko # permet de faire du SSH en code (ssh une porte sécurisée)
# ssh :un protocole pour communiquer de manière chiffrée avec une machine distante.
import getpass # permet de saisir un mot de passe sans lafficher


def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient() # creer un client ssh

    # Accepter automatiquement la clé du serveur
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connexion
    client.connect(ip, port=int(port), username=user, password=passwd)

    # Exécution de la commande
    _, stdout, stderr = client.exec_command(cmd)

    # Récupération des résultats
    output = stdout.readlines() + stderr.readlines()

    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())

    client.close()


if __name__ == '__main__':
    user = input('Username: ')
    password = getpass.getpass('Password: ')
    ip = input('Enter server IP: ') or '127.0.0.1'
    port = input('Enter port or <CR>: ') or '22'
    cmd = input('Enter command or <CR>: ') or 'whoami'

    ssh_command(ip, port, user, password, cmd)
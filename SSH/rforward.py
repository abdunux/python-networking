import socket
import select
import threading
import sys
import paramiko
import argparse
import getpass


def handler(chan, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except Exception as e:
        print(f"Forwarding request to {host}:{port} failed: {e}")
        return

    print(f"Tunnel open {chan.origin_addr} -> {chan.getpeername()} -> {(host, port)}")

    while True:
        r, w, x = select.select([sock, chan], [], [])

        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            chan.send(data)

        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)

    chan.close()
    sock.close()
    print("Tunnel closed")


def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward('', server_port)

    print(f"[+] Listening on remote port {server_port}...")

    while True:
        chan = transport.accept(1000)

        if chan is None:
            continue

        thr = threading.Thread(
            target=handler,
            args=(chan, remote_host, remote_port)
        )
        thr.setDaemon(True)
        thr.start()


def parse_options():
    parser = argparse.ArgumentParser(description='SSH Reverse Tunnel')

    parser.add_argument('--server', required=True,
                        help='SSH server address')
    parser.add_argument('--port', type=int, default=22,
                        help='SSH server port (default: 22)')
    parser.add_argument('--user', required=True,
                        help='SSH username')
    parser.add_argument('--password', action='store_true',
                        help='Ask for SSH password')
    parser.add_argument('--key', help='Private key file')

    parser.add_argument('--remote-port', type=int, required=True,
                        help='Remote port (on SSH server)')
    parser.add_argument('--target-host', required=True,
                        help='Target host (from client machine)')
    parser.add_argument('--target-port', type=int, required=True,
                        help='Target port')

    return parser.parse_args()


def main():
    options = parse_options()

    password = None
    if options.password:
        password = getpass.getpass("Enter SSH password: ")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"[+] Connecting to {options.server}:{options.port}...")

    try:
        client.connect(
            options.server,
            options.port,
            username=options.user,
            password=password,
            key_filename=options.key,
            look_for_keys=True
        )
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        sys.exit(1)

    print(f"[+] Tunnel: remote {options.server}:{options.remote_port} → {options.target_host}:{options.target_port}")

    try:
        reverse_forward_tunnel(
            options.remote_port,
            options.target_host,
            options.target_port,
            client.get_transport()
        )
    except KeyboardInterrupt:
        print("\n[!] Tunnel stopped")
        sys.exit(0)


if __name__ == '__main__':
    main()
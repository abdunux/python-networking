
import argparse  # to create a command line interface
import socket
# It splits a command string into tokens : ['echo', 'hello world']
import shlex
import subprocess  # run system commands from Python
import sys
import textwrap
import threading

#!/usr/bin/env python3

# ===================== NETCAT CLASS =====================


class NetCat:
    def __init__(self, args, buffer=None):
        # Store arguments
        self.args = args
        self.buffer = buffer

        # Create TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allow reuse of the same address/port
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Main entry point : soit serveur soit client
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
            

    # ===================== CLIENT MODE =====================
    def send(self):
        # Connect to target
        self.socket.connect((self.args.target, self.args.port))

        # Send initial buffer (if any)
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                # Receive response
                recv_len = 1
                response = ""

                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()

                    if recv_len < 4096:
                        break

                if response:
                    print(response, end="")

                # Get user input and send
                buffer = input("> ")
                buffer += "\n"
                self.socket.send(buffer.encode())

        except KeyboardInterrupt:
            print("\n[*] Connection closed.")
            self.socket.close()
            sys.exit()


    # ===================== SERVER MODE =====================
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f"[*] Listening on {self.args.target}:{self.args.port}")

        while True:
            client_socket, addr = self.socket.accept()
            print(f"[*] Connection from {addr}")

            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    # ===================== HANDLE CLIENT =====================
    def handle(self, client_socket):

        # ---- FILE UPLOAD ----
        # if self.args.upload:
        #     file_buffer = b""

        #     while True:
        #         data = client_socket.recv(4096)
                
        #         if not data:
        #             break

        #         print(f"[SERVER RECEIVED] {data.decode()}")
        #         client_socket.send(b"Message bien recu")
        #         file_buffer += data

        #     with open(self.args.upload, "wb") as f:
        #         f.write(file_buffer)

        #     client_socket.send(b"[+] File saved successfully\n")

    

        # modified : start
        if self.args.upload:
            file_buffer = b""
            
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                file_buffer += data

            with open(self.args.upload, "wb") as f:
                f.write(file_buffer)

            client_socket.send(b"[+] File saved successfully\n")

        # ---- MODE NORMAL ----
        else:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break

                print(f"[SERVER RECEIVED] {data.decode()}")
                client_socket.send(b"Message bien recu")  # END

        # ---- EXECUTE COMMAND ----
        if self.args.execute:
            output = self.execute_command(self.args.execute)
            client_socket.send(output.encode())

        # ---- INTERACTIVE SHELL ----
        if self.args.command:
            while True:
                client_socket.send(b"NC Shell> ")

                cmd_buffer = b""
                while b"\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(64)

                response = self.execute_command(cmd_buffer.decode())
                client_socket.send(response.encode())

    # ===================== RUN SYSTEM COMMAND =====================
    def execute_command(self, command):
        command = command.strip()

        if not command:
            return ""

        try:
            args = shlex.split(command)

            output = subprocess.check_output(
                args, stderr=subprocess.STDOUT
            )

            return output.decode()

        except Exception as e:
            return f"Error: {str(e)}\n"


# ===================== MAIN PROGRAM =====================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(                         # lordre du -help est : usage, description, options, epilog.
        description="Python Netcat Clone",
        # sert a choisir comment laide (-h) sera affichée dans le terminal. formatter... predefinie
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(                           # epilog signifie : texte affiche a la fin de laide + textwrap : supprimer les espaces au début des lignes (identation)
            """Examples:
  netcat.py -t 127.0.0.1 -p 5555 -l -c
  netcat.py -t 127.0.0.1 -p 5555 -l -u test.txt
  netcat.py -t 127.0.0.1 -p 5555 -l -e "cat /etc/passwd"
  echo 'Hello' | python netcat.py -t 127.0.0.1 -p 5555
  python netcat.py -t 127.0.0.1 -p 5555
"""
        ),
    )

    parser.add_argument("-c", "--command",
                        action="store_true", help="command shell")
    parser.add_argument("-e", "--execute", help="execute specified command")
    parser.add_argument(
        "-l", "--listen", action="store_true", help="listen mode")
    parser.add_argument("-p", "--port", type=int, default=5555, help="port")
    parser.add_argument(
        "-t", "--target", default="127.0.0.1", help="target IP")
    parser.add_argument("-u", "--upload", help="upload file")

    args = parser.parse_args() # here we will create arguments

    # Read stdin for client mode
    if args.listen:
        buffer = b""
    else:
        buffer = sys.stdin.read().encode()

    nc = NetCat(args, buffer)
    nc.run()

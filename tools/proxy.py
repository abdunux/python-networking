#!/usr/bin/env python3
import sys
import socket
import threading

# Create filter for printable characters
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
)


# Function to display network data in hexadecimal
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):  # src can be bytes or str
        src = src.decode(errors='replace')  # Decode bytes to string
    results = []
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(str.maketrans(HEX_FILTER, HEX_FILTER))
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length * 3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results


# Function to receive data from a socket
def receive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception:
        pass
    return buffer

# Modify packets sent by the client (optional)
def request_handler(buffer):
    # Example: buffer = buffer.replace(b"user", b"admin")
    return buffer

# Modify packets received from the server (optional)
def response_handler(buffer):
    return buffer


# Proxy handler (client ↔ proxy ↔ server)
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # Connect to remote server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # Receive from server first if required
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer):
            print(f"[<==] Sending {len(remote_buffer)} bytes to localhost.")
            client_socket.send(remote_buffer)

    # Main loop: transfer and modify data
    while True:
        # Data from client to server
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            # Display as hexdump
            print(f"[==>] Received {len(local_buffer)} bytes from localhost.")
            hexdump(local_buffer)
            # Possibility to modify via request_handler()
            local_buffer = request_handler(local_buffer)
            # Send to server (remote_socket.send)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        # Data from server to client
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print(f"[<==] Received {len(remote_buffer)} bytes from remote.")
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            # Send to client
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        # If no more data → close connections
        # If no data is received from either client
        # or server → connection terminated
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


# Server loop to accept multiple clients
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print(f"[!!] Failed to listen on {local_host}:{local_port}")
        print(f"[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print(f"[*] Listening on {local_host}:{local_port}")
    server.listen(5)
    try:
        while True:
            client_socket, addr = server.accept()
            print(f"> Received incoming connection from {addr[0]}:{addr[1]}")

            # Launch a thread for each client
            # the thread runs the proxy_handler function
            # which handles data transfer between client and server
            proxy_thread = threading.Thread(
                target=proxy_handler,
                args=(client_socket, remote_host, remote_port, receive_first)
            )
            proxy_thread.start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down proxy...")
        sys.exit(0)


# Main function
def main():
    # sys.argv = list of arguments passed to the Python script from command line
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host = sys.argv[1]  # Local IP where the proxy will listen
    local_port = int(sys.argv[2])  # Local port (converted to integer using int())
    remote_host = sys.argv[3]  # Target remote server IP
    remote_port = int(sys.argv[4])  # Target remote server port
    receive_first = sys.argv[5]  # String "True" or "False" indicating if the proxy should receive from server first before relaying client

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == '__main__':
    main()
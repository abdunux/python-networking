# Network Programming Toolkit (Python)

## Overview

This project is a Python-based network programming toolkit that demonstrates and implements core networking concepts such as TCP/UDP communication, SSH automation, port forwarding, and basic network utilities. It is designed for educational purposes and to explore low-level network operations using sockets and SSH-based techniques.

The project is organized into three main components: TCP, UDP, and advanced networking tools.

---

## Project Structure

```
project/
│
├── TCP/
│   ├── tcp_lient.py
│   └── tcp_server.py
│
├── UDP/
│   └── udp_client.py
│
├── tools/
│   ├── netcat.py
│   ├── proxy.py
    └──README.md
│
├── SSH/
    ├── ssh_cmd.py
│   ├── ssh_rcmd.py
│   ├── ssh_server.py
│   ├── rforward.py  
│   └──README.md
│
└── README.md
```

---

## Modules Description

### TCP Module

Implements reliable communication using the TCP protocol.

* `TCPClient.py`: Client-side implementation for establishing TCP connections and sending/receiving data.
* `TCPServer.py`: Server-side implementation that listens for incoming TCP connections and handles client communication.

---

### UDP Module

Implements lightweight communication using the UDP protocol.

* `udp_client.py`: Sends datagrams to a target host using UDP sockets.

---

### Tools Module

Contains advanced networking utilities and SSH-based functionalities.

* `netcat.py`: Simple network utility for reading/writing data across network connections.
* `proxy.py`: Basic proxy implementation for forwarding traffic between client and server.
* `SSHCMD.py`: Executes remote commands over SSH.
* `SSHRCMD.py`: Handles remote command execution with enhanced SSH features.
* `SSHServer.py`: SSH server implementation for handling remote connections.
* `RForward.py`: Implements SSH remote port forwarding (reverse tunneling).

---

## Requirements

* Python 3.x
* Libraries:

  * `socket`
  * `threading`
  * `select`
  * `paramiko`

Install dependencies:

```bash
pip install paramiko
```

---

## Usage

### TCP Example

```bash
python TCP/TCPServer.py
python TCP/TCPClient.py
```

### UDP Example

```bash
python UDP/UDPClient.py
```

### SSH Tools Example

```bash
python tools/SSHCMD.py
python tools/RForward.py
```

---

## Key Concepts Covered

* TCP/IP socket programming
* UDP datagram communication
* SSH automation using Paramiko
* Port forwarding and tunneling
* Client-server architecture
* Low-level network utilities

---

## Author

* GitHub: [abdunux](https://github.com/abdunux)

---

## License

This project is for educational purposes.

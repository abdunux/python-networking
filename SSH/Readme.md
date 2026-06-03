# SSH Networking Lab with Paramiko

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Paramiko](https://img.shields.io/badge/Paramiko-3.x-2E86C1?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Educational](https://img.shields.io/badge/Purpose-Educational-orange?style=flat-square)

> A collection of educational Python scripts demonstrating SSH remote administration, reverse shells, and SSH tunneling using the Paramiko library.

---

## ⚠️ Disclaimer

These scripts are intended **for educational purposes, cybersecurity training, and controlled environment experimentation only**.  
Use them exclusively on systems you own or have **explicit written authorization** to test.  
Unauthorized use is illegal and unethical.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Scripts](#scripts)
  - [ssh_cmd.py — Remote Command Execution](#1-ssh_cmdpy--remote-command-execution)
  - [ssh_rcmd.py — Reverse Shell Client](#2-ssh_rcmdpy--reverse-shell-client)
  - [ssh_server.py — Custom SSH Server](#3-ssh_serverpy--custom-ssh-server)
  - [rforward.py — Reverse Port Forwarding](#4-rforwardpy--reverse-port-forwarding)
- [Learning Objectives](#learning-objectives)
- [References](#references)
- [License](#license)

---

## Requirements

- Python 3.13.12
- [Paramiko](https://www.paramiko.org/)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ssh-networking-lab.git
cd ssh-networking-lab

# (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install paramiko
```

---

## Project Structure

```
.
├── ssh_cmd.py       # SSH client — remote command execution
├── ssh_rcmd.py      # Reverse shell client
├── ssh_server.py    # Custom SSH server for reverse shell control
└── rforward.py      # SSH reverse port forwarding
```

---

## Scripts

### 1. `ssh_cmd.py` — Remote Command Execution

Connects to a remote SSH server, authenticates with username/password, executes a single command, and displays the output.

**Usage:**

```bash
python ssh_cmd.py
```

**Example interaction:**

```
Username: user
Password:
Enter server IP: 192.168.1.10
Enter port: 22
Enter command: ls -la
```

**Architecture:**

```
Local Machine
      │
      │ SSH (port 22)
      ▼
Remote SSH Server
      │
      ▼
Command Execution → Output returned to client
```

---

### 2. `ssh_rcmd.py` — Reverse Shell Client

Establishes an outbound SSH connection to a control server. Once connected, it waits for commands, executes them locally, and returns the output through the SSH channel.

**Architecture:**

```
SSH Control Server
      │
      │ Sends commands
      ▼
ssh_rcmd.py (client machine)
      │
      │ Executes command locally
      ▼
Returns output to server
```

> **Note:** This technique is commonly used in penetration testing to bypass inbound firewall rules, as the connection is initiated from the target machine outward.

---

### 3. `ssh_server.py` — Custom SSH Server

A custom SSH server built with Paramiko that accepts incoming connections from `ssh_rcmd.py` clients. Allows an operator to send commands and receive results interactively.

**Example workflow:**

1. Start `ssh_server.py` on the control machine
2. Start `ssh_rcmd.py` on the target machine
3. Send commands from the server prompt
4. Receive and inspect results

**Architecture:**

```
Operator (terminal)
      │
      ▼
ssh_server.py (control server)
      │
      │ SSH channel
      ▼
ssh_rcmd.py (target machine)
```

---

### 4. `rforward.py` — Reverse Port Forwarding

Creates a reverse SSH tunnel that exposes a port on a remote SSH server and forwards all incoming traffic to a target host/port reachable from the client machine. Supports password or key-based authentication with multi-threaded connection handling.

**Usage:**

```bash
python rforward.py \
    --server 192.168.1.10 \
    --user user \
    --password \
    --remote-port 9000 \
    --target-host 127.0.0.1 \
    --target-port 8000
```

**What this does:**

Traffic arriving at `192.168.1.10:9000` is forwarded through the reverse SSH tunnel to `127.0.0.1:8000` on the **client machine**.

**Architecture:**

```
Remote User
      │
      ▼
SSH Server :9000
      │
      │ Reverse SSH Tunnel
      ▼
127.0.0.1:8000
(Client Machine)
```

**Use case example:** Expose a local development server (port 8000) through a cloud server without opening inbound firewall ports.

---

## Learning Objectives

This project covers the following concepts:

| Concept | Script(s) |
|---|---|
| TCP networking in Python | All |
| SSH client/server communication with Paramiko | All |
| Remote command execution | `ssh_cmd.py` |
| Reverse shell techniques | `ssh_rcmd.py`, `ssh_server.py` |
| SSH reverse tunneling | `rforward.py` |
| Port forwarding | `rforward.py` |
| Multi-threaded networking | `rforward.py` |

---

## References

- [Paramiko Documentation](https://docs.paramiko.org/)
- [SSH Protocol — RFC 4251](https://www.rfc-editor.org/rfc/rfc4251)
- *Black Hat Python* — Justin Seitz & Tim Arnold (No Starch Press)

---

## License

This project is licensed under the [MIT License](LICENSE).  
Use responsibly and ethically.
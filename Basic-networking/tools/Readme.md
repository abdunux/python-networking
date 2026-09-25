# tools/

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Educational](https://img.shields.io/badge/Purpose-Educational-orange?style=flat-square)

> Low-level TCP networking tools written in pure Python — a Netcat clone and a TCP proxy with hexdump inspection.

---

## ⚠️ Disclaimer

These tools are intended **for educational purposes, cybersecurity training, and controlled environment experimentation only**.  
Use them exclusively on systems you own or have **explicit written authorization** to test.  
Unauthorized use is illegal and unethical.

---

## Table of Contents

- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Tools](#tools)
  - [netcat.py — Netcat Clone](#1-netcatpy--netcat-clone)
  - [proxy.py — TCP Proxy](#2-proxypy--tcp-proxy)
- [Learning Objectives](#learning-objectives)
- [References](#references)

---

## Requirements

- Python 3.8+
- Standard library only — **no external dependencies**

---

## Project Structure

```
tools/
├── netcat.py    # Multi-mode Netcat clone (client, server, shell, upload)
└── proxy.py     # TCP proxy with hexdump inspection and traffic manipulation
```

---

## Tools

### 1. `netcat.py` — Netcat Clone

A fully functional Netcat reimplementation supporting client mode, server mode, interactive shell, command execution, and file upload. All modes are controlled via command-line flags.

#### Modes

| Flag | Description |
|---|---|
| `-l` / `--listen` | Listen mode (server) |
| `-c` / `--command` | Spawn an interactive command shell |
| `-e` / `--execute CMD` | Execute a single command on connection |
| `-u` / `--upload FILE` | Save received data to a file |
| `-t` / `--target IP` | Target host (default: `127.0.0.1`) |
| `-p` / `--port PORT` | Port (default: `5555`) |

#### Architecture

```
                    CLIENT MODE
┌─────────────┐   TCP connect   ┌──────────────────┐
│  netcat.py  │ ──────────────► │   Remote Server  │
│  (client)   │ ◄────────────── │                  │
└─────────────┘   send/receive  └──────────────────┘

                    SERVER MODE
┌─────────────┐   TCP accept    ┌──────────────────┐
│  netcat.py  │ ◄────────────── │   Remote Client  │
│  (server)   │ ──────────────► │                  │
└─────────────┘   handle/reply  └──────────────────┘
```

#### Usage examples

```bash
# Start an interactive shell server on port 5555
python netcat.py -t 127.0.0.1 -p 5555 -l -c

# Execute a command on incoming connection
python netcat.py -t 127.0.0.1 -p 5555 -l -e "cat /etc/passwd"

# Receive and save an uploaded file
python netcat.py -t 127.0.0.1 -p 5555 -l -u received.txt

# Send a message as a client
echo 'Hello' | python netcat.py -t 127.0.0.1 -p 5555

# Open an interactive client session
python netcat.py -t 127.0.0.1 -p 5555
```

---

### 2. `proxy.py` — TCP Proxy

A transparent TCP proxy that sits between a client and a remote server. It captures, displays (hexdump), and optionally modifies all traffic flowing in both directions. Useful for protocol analysis and traffic inspection.

#### How it works

1. The proxy listens on a local port
2. For each incoming client connection, it opens a corresponding connection to the remote server
3. All data flowing in both directions is captured and displayed as a hexdump
4. Two hooks — `request_handler()` and `response_handler()` — allow inline packet modification
5. Each client connection is handled in a dedicated thread

#### Architecture

```
┌──────────┐  local traffic   ┌───────────────┐  remote traffic  ┌──────────────┐
│  Client  │ ───────────────► │               │ ───────────────► │    Remote    │
│          │                  │   proxy.py    │                  │    Server    │
│          │ ◄─────────────── │  (intercept)  │ ◄─────────────── │              │
└──────────┘  modified reply  └───────────────┘  original reply  └──────────────┘
                                     │
                                     ▼
                              hexdump output
                          (inspect every byte)
```

#### Usage

```bash
python proxy.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]
```

| Argument | Description |
|---|---|
| `local_host` | IP address the proxy will bind to |
| `local_port` | Port the proxy will listen on |
| `remote_host` | IP of the target remote server |
| `remote_port` | Port of the target remote server |
| `receive_first` | `True` if the server speaks first (e.g. FTP, SMTP), `False` otherwise |

#### Example

```bash
# Intercept traffic between local port 9000 and a remote server at 10.12.132.1:9000
python proxy.py 127.0.0.1 9000 10.12.132.1 9000 True
```

#### Hexdump output format

```
0000  48 65 6C 6C 6F 20 57 6F  72 6C 64 0A             Hello World.
```

Each line shows: offset · hex bytes · printable ASCII representation.

#### Customizing traffic

Open `proxy.py` and edit the two handler functions:

```python
def request_handler(buffer):
    # Modify client → server traffic here
    # Example: buffer = buffer.replace(b"user", b"admin")
    return buffer

def response_handler(buffer):
    # Modify server → client traffic here
    return buffer
```

---

## Learning Objectives

| Concept | Tool(s) |
|---|---|
| Raw TCP socket programming | Both |
| Multi-threaded server design | Both |
| Binary data inspection (hexdump) | `proxy.py` |
| Traffic interception and modification | `proxy.py` |
| Interactive shell over network | `netcat.py` |
| File transfer over raw TCP | `netcat.py` |
| CLI design with `argparse` | `netcat.py` |
| Subprocess execution from network input | `netcat.py` |

---

## References

- [Python `socket` documentation](https://docs.python.org/3/library/socket.html)
- [Python `subprocess` documentation](https://docs.python.org/3/library/subprocess.html)
- *Black Hat Python* — Justin Seitz & Tim Arnold (No Starch Press)
- [RFC 793 — Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc793)
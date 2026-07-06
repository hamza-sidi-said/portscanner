# Simple Port Scanner

A beginner-friendly TCP port scanner written in Python. It scans a range of
ports on a target IP or domain and reports whether each port is **OPEN**,
**CLOSED**, or **FILTERED**. If a port is open, it also tries to grab a
"banner" — a bit of text the service sends back — which can hint at what
software is running on that port.

## How it works

For each port in the given range, the script tries to open a TCP
connection to the target:

- If the connection succeeds → the port is **OPEN**.
- If the connection is refused → the port is **CLOSED**.
- If the connection times out with no response → the port is **FILTERED**
  (usually means a firewall is silently dropping the packets).

To scan faster, ports are checked in parallel using a thread pool instead
of one at a time.

## Requirements

- Python 3.7 or higher
- No external libraries needed (uses only the standard library)

## Usage

```bash
python port_scanner.py <target> <start_port> <end_port> [--threads N]
```

**Arguments**

| Argument      | Description                                  |
|---------------|-----------------------------------------------|
| `target`      | IP address or domain name to scan             |
| `start_port`  | First port in the range to scan               |
| `end_port`    | Last port in the range to scan                |
| `--threads`   | (Optional) How many ports to check at once. Default: 50 |

**Examples**

```bash
# Scan ports 20-100 on a domain
python port_scanner.py scanme.nmap.org 20 100

# Scan the first 1024 ports on a local machine, faster with more threads
python port_scanner.py 192.168.1.10 1 1024 --threads 100
```

## Example output

```
Target : scanme.nmap.org
IP     : 45.33.32.156
Ports  : 20-25
Threads: 50

Results:

[-] Port 20 is CLOSED
[-] Port 21 is CLOSED
[+] Port 22 (SSH) is OPEN
    Banner: SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
[-] Port 23 is CLOSED
[-] Port 24 is CLOSED
[-] Port 25 is CLOSED
```

## ⚠️ Legal / Ethical Notice

Only scan systems you **own** or have **explicit permission** to test.
Scanning networks without authorization is illegal in many countries and
against the terms of service of most hosting providers. This project is
for educational purposes only (e.g. learning about sockets, networking,
and how port scanners work).

A safe target for practice is `scanme.nmap.org`, which is provided by the
Nmap project specifically for testing scanners.

## Possible improvements (ideas for extending the project)

- Add UDP scanning support
- Export results to a CSV or JSON file
- Add a `--verbose` flag to show closed ports too
- Add service/version detection for more ports
- Add a simple progress bar.
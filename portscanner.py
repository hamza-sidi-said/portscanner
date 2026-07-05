#!/usr/bin/env python3
"""
Simple Port Scanner
--------------------
A basic educational TCP port scanner written for learning purposes.
It attempts to connect to a range of ports on a target host and
reports whether each port is OPEN, CLOSED, or FILTERED.
For open ports, it tries to grab a simple banner (works well for
HTTP, and often for other text-based protocols like FTP/SMTP).
"""

import socket
import argparse


def grab_banner(sock, ip, port):
    """Try to read a banner from an open port. Sends an HTTP request for port 80/443-like ports."""
    try:
        if port in (80, 8080):
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n"
            sock.send(request.encode())
        data = sock.recv(1024)
        if data:
            return data.decode("utf-8", errors="ignore").strip()
        return None
    except socket.timeout:
        return None
    except Exception:
        return None


def scan_port(ip, port, timeout=2):
    """Scan a single port and print its status."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((ip, port))
            print(f"[+] Port {port:<5} OPEN")

            banner = grab_banner(s, ip, port)
            if banner:
                print("    Banner:")
                for line in banner.splitlines()[:5]:  # limit output
                    print(f"    {line}")
            else:
                print("    No banner received.")

        except ConnectionRefusedError:
            print(f"[-] Port {port:<5} CLOSED")
        except socket.timeout:
            print(f"[!] Port {port:<5} FILTERED")


def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="IP address or domain to scan")
    parser.add_argument("start_port", type=int, help="Starting port")
    parser.add_argument("end_port", type=int, help="Ending port")
    parser.add_argument(
        "-t", "--timeout", type=float, default=2.0,
        help="Connection timeout in seconds (default: 2.0)"
    )
    args = parser.parse_args()

    if args.start_port > args.end_port:
        print("Error: start_port must be <= end_port")
        return

    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("Invalid domain or IP address.")
        return

    print(f"Target : {args.target}")
    print(f"IP     : {ip}")
    print(f"Ports  : {args.start_port}-{args.end_port}\n")

    for port in range(args.start_port, args.end_port + 1):
        scan_port(ip, port, timeout=args.timeout)

    print("\nScan complete.")


if __name__ == "__main__":
    main()
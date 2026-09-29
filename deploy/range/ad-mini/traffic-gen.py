"""Fake network traffic generator for the AD mini range.

Emits periodic SMB/Kerberos-like TCP probes plus fake user logons so junior
operators practice implant deployment and lateral movement against a noisy,
legal, fully local background. Targets resolve over the compose network,
so no fixed subnet is required.
"""

from __future__ import annotations

import random
import socket
import time

TARGETS = [("dc", 445), ("dc", 389), ("ws01", 80)]
USERS = ["jdoe", "asmith", "svc_backup", "helpdesk", "mgarcia"]
BASE_DELAY = 30
JITTER = 15


def _probe(host: str, port: int) -> None:
    """Attempt one short TCP connection, ignoring failures.

    Args:
        host: Target hostname on the range network.
        port: Target TCP port.
    """
    try:
        with socket.create_connection((host, port), timeout=3):
            pass
    except OSError:
        pass


def main() -> None:
    """Loop forever emitting fake background traffic."""
    while True:
        host, port = random.choice(TARGETS)
        _probe(host, port)
        user = random.choice(USERS)
        print(f"[traffic] fake logon {user} probe {host}:{port}", flush=True)
        time.sleep(BASE_DELAY + random.randint(-JITTER, JITTER))


if __name__ == "__main__":
    main()

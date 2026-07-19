"""Network primitives for the LazyOwn framework.

Extracted from ``utils.py`` — ARP spoofing, socket operations, port
detection, and network parsing utilities.
"""

from __future__ import annotations

import binascii
import re
import socket
import struct
from typing import Any

from core.console import print_error


def parse_ip_mac(input_string: str) -> tuple[str | None, str | None]:
    """Extract IP and MAC from a formatted string.

    Expected format: ``IP: (192.168.1.222) MAC: ec:c3:02:b0:4c:96``

    Returns:
        ``(ip, mac)`` tuple or ``(None, None)`` on failure.
    """
    match = re.match(
        r"IP:\s*\(([\d.]+)\)\s*MAC:\s*([\da-f:]+)", input_string.strip()
    )
    if match:
        return match.groups()
    print_error(
        "Error: Input must be in the format "
        "'IP: (192.168.1.222) MAC: ec:c3:02:b0:4c:96'."
    )
    return None, None


def create_arp_packet(
    src_mac: str, src_ip: str, dst_ip: str, dst_mac: str
) -> bytes:
    """Build a raw ARP request/reply packet.

    Args:
        src_mac: Source MAC (``xx:xx:xx:xx:xx:xx``).
        src_ip: Source IP (dotted decimal).
        dst_ip: Destination IP.
        dst_mac: Destination MAC.

    Returns:
        Raw Ethernet + ARP frame bytes.
    """
    eth_header = struct.pack(
        "!6s6sH",
        binascii.unhexlify(dst_mac.replace(":", "")),
        binascii.unhexlify(src_mac.replace(":", "")),
        0x0806,
    )
    arp_header = struct.pack(
        "!HHBBH6s4s6s4s",
        0x0001,
        0x0800,
        6,
        4,
        0x0002,
        binascii.unhexlify(src_mac.replace(":", "")),
        socket.inet_aton(src_ip),
        binascii.unhexlify(dst_mac.replace(":", "")),
        socket.inet_aton(dst_ip),
    )
    return eth_header + arp_header


def send_packet(packet: bytes, iface: str) -> None:
    """Send a raw packet on a given network interface.

    Args:
        packet: Raw frame bytes.
        iface: Interface name (e.g. ``eth0``).
    """
    with socket.socket(
        socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0806)
    ) as sock:
        sock.bind((iface, 0))
        sock.send(packet)


def parse_proc_net_file(file_path: str) -> list[tuple[str, int]]:
    """Parse a ``/proc/net/*`` file and extract (ip, port) pairs.

    Args:
        file_path: Path to a ``/proc/net/tcp``-style file.

    Returns:
        List of ``(ip_address, port)`` tuples.
    """
    entries: list[tuple[str, int]] = []
    try:
        with open(file_path, encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                local_address = parts[1]
                ip_hex, port_hex = local_address.split(":")
                ip_parts = [
                    int(ip_hex[i : i + 2], 16)
                    for i in range(0, len(ip_hex), 2)
                ]
                ip_address = ".".join(str(p) for p in ip_parts)
                port = int(port_hex, 16)
                entries.append((ip_address, port))
    except (FileNotFoundError, PermissionError, IndexError, ValueError):
        pass
    return entries


def get_open_ports() -> list[tuple[str, int]]:
    """Discover listening TCP ports from ``/proc/net/tcp`` and ``tcp6``.

    Returns:
        List of ``(ip, port)`` tuples for listening endpoints.
    """
    open_ports: list[tuple[str, int]] = []
    for net_file in ["/proc/net/tcp", "/proc/net/tcp6"]:
        entries = parse_proc_net_file(net_file)
        for ip, port in entries:
            if ip == "0.0.0.0" or ip == "::" or ip.startswith("127"):
                open_ports.append((ip, port))
    return open_ports


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Check whether a TCP port is already bound.

    Args:
        port: Port number.
        host: Host to check (default ``127.0.0.1``).

    Returns:
        True if the port is in use.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((host, port)) == 0


def get_banner(ip: str, port: int) -> str:
    """Grab a TCP banner from the given host and port.

    Args:
        ip: Target IP.
        port: Target port.

    Returns:
        Banner string, or an empty string on failure.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip, port))
            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            return banner
    except (TimeoutError, ConnectionRefusedError, OSError):
        return ""


def get_network_info() -> dict[str, Any]:
    """Collect local network information.

    Returns:
        Dict with keys ``hostname``, ``ips``, ``interfaces``.
    """
    import netifaces
    info: dict[str, Any] = {"hostname": socket.gethostname(), "ips": [], "interfaces": {}}
    try:
        info["ips"].append(socket.gethostbyname(socket.gethostname()))
    except socket.gaierror:
        pass
    try:
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            info["interfaces"][iface] = {
                k: [a.get("addr") for a in v if a.get("addr")]
                for k, v in addrs.items()
            }
            if netifaces.AF_INET in addrs:
                for a in addrs[netifaces.AF_INET]:
                    ip = a.get("addr")
                    if ip and ip not in info["ips"]:
                        info["ips"].append(ip)
    except Exception:
        pass
    return info


__all__ = [
    "create_arp_packet",
    "get_banner",
    "get_network_info",
    "get_open_ports",
    "is_port_in_use",
    "parse_ip_mac",
    "parse_proc_net_file",
    "send_packet",
]

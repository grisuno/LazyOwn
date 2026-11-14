"""Canonical nmap XML fingerprinting for the exploit stack.

Single parser and service model shared by ``modules.exploit_chain``
(recon-to-vuln pipeline) and ``cli.exploit_advisor`` (``ss`` command
surface), so token shapes and XML handling cannot drift. Parsing uses
``defusedxml`` everywhere: scan artefacts are untrusted input.
"""

from __future__ import annotations

import glob
import os
from dataclasses import dataclass

import defusedxml.ElementTree as ET

SERVICE_NEXT_COMMANDS: dict[str, list[tuple[str, str]]] = {
    "ssh": [
        ("lazyssh77enum", "Username enumeration via timing"),
        ("hydra", "Brute-force login"),
        ("lazyreverse_shell", "Drop shell if creds known"),
    ],
    "http": [
        ("gobuster", "Directory enumeration"),
        ("ffuf", "Fuzzing"),
        ("nikto", "Vulnerability scan"),
        ("whatweb", "Tech fingerprint"),
        ("dirsearch", "Deep content discovery"),
    ],
    "https": [
        ("gobuster", "Directory enumeration"),
        ("ffuf", "Fuzzing"),
        ("nikto", "Vulnerability scan"),
        ("sslscan", "TLS/SSL audit"),
        ("whatweb", "Tech fingerprint"),
    ],
    "ftp": [("lazyftpsniff", "Sniff FTP credentials"), ("hydra", "Brute-force login — try anonymous first")],
    "smb": [
        ("enum4linux_ng", "Full SMB enumeration"),
        ("smbclient", "Browse shares"),
        ("crackmapexec", "CME spray"),
        ("bloodhound", "AD attack paths"),
    ],
    "microsoft-ds": [
        ("enum4linux_ng", "Full SMB enumeration"),
        ("smbclient", "Browse shares"),
        ("crackmapexec", "CME spray"),
    ],
    "netbios-ssn": [("enum4linux", "NetBIOS enumeration"), ("smbclient", "Browse shares")],
    "msrpc": [("rpcclient", "Null-session RPC enum"), ("enum4linux", "Full enumeration")],
    "mysql": [("sqlmap", "SQL injection testing"), ("hydra", "Brute-force login")],
    "mssql": [("sqlmap", "SQL injection"), ("crackmapexec", "CME mssql module"), ("lazymetasploit", "MSF mssql_login")],
    "postgresql": [("sqlmap", "SQL injection"), ("hydra", "Brute-force login")],
    "rdp": [("xfreerdp", "Connect if creds known"), ("hydra", "Brute-force login"), ("rdp_check", "Check NLA/version")],
    "ms-wbt-server": [("xfreerdp", "RDP connection"), ("hydra", "Brute-force")],
    "winrm": [("evil_winrm", "WinRM shell if creds known"), ("crackmapexec", "CME winrm check")],
    "wsman": [("evil_winrm", "WinRM shell"), ("crackmapexec", "CME winrm check")],
    "ldap": [
        ("windapsearch", "LDAP anonymous enum"),
        ("ldapsearch", "Raw LDAP queries"),
        ("bloodhound", "AD attack paths"),
    ],
    "ldapssl": [("windapsearch", "LDAP enum over SSL"), ("bloodhound", "AD attack paths")],
    "kerberos-sec": [
        ("kerbrute", "Username enumeration"),
        ("asrep_roasting", "ASREPRoast no-preauth users"),
        ("kerberoasting", "Kerberoast SPNs"),
    ],
    "kpasswd5": [("kerbrute", "Kerberos password spray")],
    "snmp": [("snmpwalk", "SNMP walk community strings"), ("lazysniff", "Packet capture")],
    "nfs": [("showmount", "List NFS exports"), ("lazynmap", "Enumerate mount paths")],
    "pop3": [("hydra", "Brute-force POP3"), ("telnet", "Manual banner grab")],
    "smtp": [("smtp_enum", "SMTP user enumeration"), ("swaks", "SMTP relay test")],
    "imap": [("hydra", "Brute-force IMAP"), ("curl", "Manual IMAP browse")],
    "vnc": [("hydra", "Brute-force VNC"), ("lazymetasploit", "MSF vnc_login")],
    "redis": [("redis-cli", "Unauthenticated access check"), ("lazymetasploit", "MSF redis_server")],
    "mongodb": [("mongosh", "Unauthenticated access check"), ("lazymetasploit", "MSF mongodb_login")],
    "elasticsearch": [("curl", "Check /_cat/indices for open cluster"), ("lazymetasploit", "MSF elasticsearch_unauth")],
    "docker": [("docker", "Remote Docker API abuse — unauthenticated RCE risk")],
    "kubernetes": [("kubectl", "K8s API server access check")],
    "ssl/http": [
        ("gobuster", "Directory enumeration"),
        ("ffuf", "Fuzzing"),
        ("sslscan", "TLS/SSL audit"),
        ("nikto", "Vulnerability scan"),
    ],
    "https?": [("gobuster", "Directory enumeration"), ("ffuf", "Fuzzing"), ("nikto", "Vulnerability scan")],
}

FALLBACK_COMMANDS: list[tuple[str, str]] = [
    ("lazynmap", "Deep service version scan"),
    ("ss", "Search for exploits: ss <service> <version>"),
    ("searchsploit", "Direct searchsploit query"),
]


@dataclass
class ServiceInfo:
    """One open port with its service fingerprint."""

    port: int
    protocol: str = "tcp"
    name: str = ""
    product: str = ""
    version: str = ""
    extra_info: str = ""

    @property
    def search_query(self) -> str:
        """Best query string for searchsploit / NVD."""
        parts = [p for p in (self.product or self.name, self.version) if p]
        return " ".join(parts)

    @property
    def display_name(self) -> str:
        """Human-readable service label for operator tables."""
        parts = [p for p in (self.product or self.name, self.version) if p]
        return " ".join(parts) or self.name

    def next_commands(self) -> list[tuple[str, str]]:
        """Return (command, reason) pairs recommended for this service."""
        for key in (self.name.lower(), (self.product or "").lower()):
            if key and key in SERVICE_NEXT_COMMANDS:
                return SERVICE_NEXT_COMMANDS[key]
        for key, cmds in SERVICE_NEXT_COMMANDS.items():
            if key in self.name.lower():
                return cmds
        return FALLBACK_COMMANDS


def parse_nmap_xml(path: str) -> list[ServiceInfo]:
    """Extract open services from a nmap XML file.

    Args:
        path: Path to the .nmap.xml file.

    Returns:
        One :class:`ServiceInfo` per open TCP/UDP port found; parse
        errors yield an empty list so a torn file never aborts a run.
    """
    services: list[ServiceInfo] = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except (ET.ParseError, OSError):
        return services
    for host in root.findall("host"):
        for port_el in host.findall("ports/port"):
            state_el = port_el.find("state")
            if state_el is None or state_el.get("state") != "open":
                continue
            svc_el = port_el.find("service")
            services.append(
                ServiceInfo(
                    port=int(port_el.get("portid", 0)),
                    protocol=port_el.get("protocol", "tcp"),
                    name=svc_el.get("name", "") if svc_el is not None else "",
                    product=svc_el.get("product", "") if svc_el is not None else "",
                    version=svc_el.get("version", "") if svc_el is not None else "",
                    extra_info=svc_el.get("extrainfo", "") if svc_el is not None else "",
                )
            )
    return services


def find_nmap_xml(rhost: str, sessions_dir: str = "sessions", include_vulns: bool = False) -> list[str]:
    """Return nmap XML files for a given rhost.

    Args:
        rhost: Target IP to filter on.
        sessions_dir: Path to the sessions directory.
        include_vulns: Also include ``vulns_<rhost>*`` scan artefacts
            (exploit-chain merge input); the advisor surface reads only
            ``scan_<rhost>*``, newest first.

    Returns:
        Sorted list of paths (newest first for the scan-only surface).
    """
    patterns = [f"{sessions_dir}/scan_{rhost}*.nmap.xml"]
    if include_vulns:
        patterns.append(f"{sessions_dir}/vulns_{rhost}*.nmap.xml")
    files = [path for pattern in patterns for path in glob.glob(pattern)]
    if not include_vulns:
        files.sort(key=os.path.getmtime, reverse=True)
    return files


__all__ = ["FALLBACK_COMMANDS", "SERVICE_NEXT_COMMANDS", "ServiceInfo", "find_nmap_xml", "parse_nmap_xml"]

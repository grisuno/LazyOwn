#!/usr/bin/env python3
"""
LazyOwn FactStore
=================
Structured fact extraction from nmap XML files and pwntomate tool output.

Reads  sessions/scan_*.nmap.xml   → host/port/service facts
Reads  sessions/*.txt              → credentials, shares, access-level hints
Writes sessions/policy_facts.json  → single merged fact store

Consumed by lazyown_mcp.py auto_loop to parameterise commands with
real discovered data instead of generic category defaults.

Usage:
    python3 skills/lazyown_facts.py parse [--target TARGET]
    python3 skills/lazyown_facts.py show  [--target TARGET]
    python3 skills/lazyown_facts.py clean
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


# ─── Config ──────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Config:
    """All file paths and constants for the FactStore."""

    base_dir: Path
    sessions_dir: Path
    facts_file: Path
    xml_glob: str
    txt_glob: str
    log_level: str

    @classmethod
    def default(cls) -> "Config":
        base = Path(__file__).parent.parent
        sessions = base / "sessions"
        return cls(
            base_dir=base,
            sessions_dir=sessions,
            facts_file=sessions / "policy_facts.json",
            xml_glob="scan_*.nmap.xml",
            txt_glob="*.txt",
            log_level="WARNING",
        )


# ─── Data models ─────────────────────────────────────────────────────────────


@dataclass
class ServiceFact:
    """A single open port on a host."""

    host: str
    port: int
    protocol: str
    service: str
    product: str
    version: str
    state: str


@dataclass
class CredentialFact:
    """A credential pair discovered by any tool."""

    host: str
    username: str
    password: str
    source_file: str
    hash_value: str = ""
    hash_type: str = ""


@dataclass
class ShareFact:
    """A network share."""

    host: str
    share_name: str
    access: str
    source_file: str


@dataclass
class AccessFact:
    """Evidence of access to a host."""

    host: str
    level: str
    method: str
    source_file: str


@dataclass
class VulnerabilityFact:
    """A vulnerability or weakness found on a host."""
    host: str
    vuln_id: str        # CVE-XXXX-XXXX or OSVDB-XXXX or template-id
    severity: str       # critical / high / medium / low / info
    title: str
    url: str
    source_tool: str
    source_file: str


@dataclass
class DiscoveredPath:
    """A web path found by directory enumeration."""
    host: str
    port: int
    path: str
    status_code: int
    size: int
    source_file: str


@dataclass
class HostFacts:
    """All known facts for a single target IP."""

    host: str
    services: List[ServiceFact] = field(default_factory=list)
    credentials: List[CredentialFact] = field(default_factory=list)
    shares: List[ShareFact] = field(default_factory=list)
    access: List[AccessFact] = field(default_factory=list)
    raw_files: List[str] = field(default_factory=list)
    vulnerabilities: List[VulnerabilityFact] = field(default_factory=list)
    paths: List[DiscoveredPath] = field(default_factory=list)
    os_hint: str = ""

    def highest_access(self) -> str:
        if not self.access:
            return "none"
        order = ["none", "read", "write", "user", "admin", "system", "root"]
        levels = [a.level.lower() for a in self.access]
        best = "none"
        for lvl in levels:
            if lvl in order and order.index(lvl) > order.index(best):
                best = lvl
        return best

    def open_ports(self) -> List[int]:
        return sorted({s.port for s in self.services if s.state == "open"})

    def services_by_name(self, name: str) -> List[ServiceFact]:
        return [s for s in self.services if name.lower() in s.service.lower()]


# ─── Parsers ─────────────────────────────────────────────────────────────────


class INmapXmlParser:
    """Parse a single nmap XML file into ServiceFact objects."""

    def parse(self, xml_path: Path) -> List[ServiceFact]:
        facts: List[ServiceFact] = []
        try:
            tree = ET.parse(str(xml_path))
        except ET.ParseError:
            return facts
        root = tree.getroot()
        for host_el in root.iter("host"):
            addr_el = host_el.find("address")
            if addr_el is None:
                continue
            ip = addr_el.get("addr", "")
            if not ip:
                continue
            ports_el = host_el.find("ports")
            if ports_el is None:
                continue
            for port_el in ports_el.findall("port"):
                state_el = port_el.find("state")
                if state_el is None or state_el.get("state") != "open":
                    continue
                service_el = port_el.find("service")
                svc_name = ""
                product = ""
                version = ""
                if service_el is not None:
                    svc_name = service_el.get("name", "")
                    product = service_el.get("product", "")
                    version = service_el.get("version", "")
                facts.append(
                    ServiceFact(
                        host=ip,
                        port=int(port_el.get("portid", 0)),
                        protocol=port_el.get("protocol", "tcp"),
                        service=svc_name,
                        product=product,
                        version=version,
                        state="open",
                    )
                )
        return facts


class ITextOutputParser:
    """Base class for tool-output text parsers."""

    TOOL_NAME: str = ""

    def can_parse(self, filename: str, content: str) -> bool:  # noqa: D102
        raise NotImplementedError

    def parse(
        self,
        host: str,
        content: str,
        source_file: str,
    ) -> tuple[List[CredentialFact], List[ShareFact], List[AccessFact]]:
        raise NotImplementedError

    def parse_extended(
        self,
        host: str,
        content: str,
        source_file: str,
        port: int = 80,
    ) -> "tuple[List[CredentialFact], List[ShareFact], List[AccessFact], List[VulnerabilityFact], List[DiscoveredPath]]":
        """Extended parse including vulnerabilities and web paths. Override in subclasses."""
        creds, shares, access = self.parse(host, content, source_file)
        return creds, shares, access, [], []


class CrackMapExecParser(ITextOutputParser):
    """Parse crackmapexec / nxc output."""

    TOOL_NAME = "crackmapexec"

    _CRED_RE = re.compile(
        r"(?P<host>[\d.]+)\s+\d+\s+\S+\s+\[\+\]\s+\S+\\(?P<user>\S+):(?P<pass>\S+)"
    )
    _PWNED_RE = re.compile(r"Pwn3d!")
    _SHARE_RE = re.compile(
        r"(?P<host>[\d.]+)\s+\d+\s+\S+\s+\[-\]\s+\S+\\(?P<share>\S+)\s+(?P<access>\S+)"
    )
    _SHARE2_RE = re.compile(
        r"(?P<share>\S+)\s+READ(?P<write>(?:,WRITE)?)"
    )

    def can_parse(self, filename: str, content: str) -> bool:
        return "crackmapexec" in filename.lower() or "nxc" in filename.lower() or (
            re.search(r"SMB\s+[\d.]+\s+\d+", content) is not None
        )

    def parse(self, host: str, content: str, source_file: str):
        creds: List[CredentialFact] = []
        shares: List[ShareFact] = []
        access: List[AccessFact] = []
        for m in self._CRED_RE.finditer(content):
            creds.append(CredentialFact(
                host=m.group("host") or host,
                username=m.group("user"),
                password=m.group("pass"),
                source_file=source_file,
            ))
        if self._PWNED_RE.search(content):
            access.append(AccessFact(
                host=host,
                level="admin",
                method="crackmapexec",
                source_file=source_file,
            ))
        for m in self._SHARE2_RE.finditer(content):
            write = bool(m.group("write"))
            shares.append(ShareFact(
                host=host,
                share_name=m.group("share"),
                access="READ+WRITE" if write else "READ",
                source_file=source_file,
            ))
        return creds, shares, access


class Enum4linuxParser(ITextOutputParser):
    """Parse enum4linux / enum4linux-ng output."""

    TOOL_NAME = "enum4linux"

    _USER_RE = re.compile(r"user:\[(?P<user>[^\]]+)\]\s+rid:\[\w+\]")
    _SHARE_RE = re.compile(
        r"\|\s+(?P<share>\S+)\s+\|\s+(?P<type>Disk|IPC|Printer)\s*\|\s+(?P<comment>.*?)\s*\|"
    )
    _PASS_RE = re.compile(r"Password:\s+(?P<pass>\S+)")

    def can_parse(self, filename: str, content: str) -> bool:
        return "enum4linux" in filename.lower() or "enum_smb" in filename.lower()

    def parse(self, host: str, content: str, source_file: str):
        creds: List[CredentialFact] = []
        shares: List[ShareFact] = []
        access: List[AccessFact] = []
        for m in self._USER_RE.finditer(content):
            creds.append(CredentialFact(
                host=host,
                username=m.group("user").strip(),
                password="",
                source_file=source_file,
            ))
        for m in self._SHARE_RE.finditer(content):
            shares.append(ShareFact(
                host=host,
                share_name=m.group("share").strip(),
                access=m.group("type").strip(),
                source_file=source_file,
            ))
        if creds or shares:
            access.append(AccessFact(
                host=host, level="read", method="enum4linux", source_file=source_file
            ))
        return creds, shares, access


class SecretsdumpParser(ITextOutputParser):
    """Parse impacket secretsdump output."""

    TOOL_NAME = "secretsdump"

    _NTLM_RE = re.compile(
        r"(?P<domain>\S+)\\(?P<user>[^:]+):(?P<rid>\d+):(?P<lm>[0-9a-fA-F]{32}):(?P<nt>[0-9a-fA-F]{32}):::"
    )
    _CLEARTEXT_RE = re.compile(
        r"(?P<domain>\S+)\\(?P<user>[^:]+):\w+:(?P<pass>.+)"
    )

    def can_parse(self, filename: str, content: str) -> bool:
        return "secretsdump" in filename.lower() or (
            re.search(r"[0-9a-fA-F]{32}:[0-9a-fA-F]{32}:::", content) is not None
        )

    def parse(self, host: str, content: str, source_file: str):
        creds: List[CredentialFact] = []
        shares: List[ShareFact] = []
        access: List[AccessFact] = []
        for m in self._NTLM_RE.finditer(content):
            creds.append(CredentialFact(
                host=host,
                username=m.group("user").strip(),
                password="",
                source_file=source_file,
                hash_value=m.group("nt"),
                hash_type="NTLM",
            ))
        if creds:
            access.append(AccessFact(
                host=host, level="admin", method="secretsdump", source_file=source_file
            ))
        return creds, shares, access


class LdapParser(ITextOutputParser):
    """Parse ldapsearch / ldapdomaindump output."""

    TOOL_NAME = "ldap"

    _DN_RE = re.compile(r"dn:\s+(?P<dn>CN=[^,]+,.*)")
    _SAM_RE = re.compile(r"sAMAccountName:\s+(?P<sam>\S+)")

    def can_parse(self, filename: str, content: str) -> bool:
        return any(k in filename.lower() for k in ("ldap", "ldapdomaindump"))

    def parse(self, host: str, content: str, source_file: str):
        creds: List[CredentialFact] = []
        shares: List[ShareFact] = []
        access: List[AccessFact] = []
        for m in self._SAM_RE.finditer(content):
            creds.append(CredentialFact(
                host=host,
                username=m.group("sam"),
                password="",
                source_file=source_file,
            ))
        if creds:
            access.append(AccessFact(
                host=host, level="read", method="ldapsearch", source_file=source_file
            ))
        return creds, shares, access


class KerbruteParser(ITextOutputParser):
    """Parse kerbrute user enumeration output."""

    TOOL_NAME = "kerbrute"

    _VALID_RE  = re.compile(r"VALID\s+USERNAME:\s*(\S+?)@\S+", re.IGNORECASE)
    _VALID2_RE = re.compile(r"\[\+\]\s+(\S+)\s+is valid", re.IGNORECASE)

    def can_parse(self, filename: str, content: str) -> bool:
        return "kerbrute" in filename.lower() or "VALID USERNAME" in content

    def parse(self, host: str, content: str, source_file: str):
        creds: List[CredentialFact] = []
        for m in self._VALID_RE.finditer(content):
            creds.append(CredentialFact(
                host=host, username=m.group(1), password="", source_file=source_file
            ))
        for m in self._VALID2_RE.finditer(content):
            creds.append(CredentialFact(
                host=host, username=m.group(1), password="", source_file=source_file
            ))
        access = (
            [AccessFact(host=host, level="read", method="kerbrute", source_file=source_file)]
            if creds else []
        )
        return creds, [], access


class RpcclientParser(ITextOutputParser):
    """Parse rpcclient / enum_rpcbind output."""

    TOOL_NAME = "rpcclient"

    _USER_RE  = re.compile(r"user:\[([^\]]+)\]\s+rid:\[0x[\da-fA-F]+\]")
    _GROUP_RE = re.compile(r"group:\[([^\]]+)\]\s+rid:\[0x[\da-fA-F]+\]")

    def can_parse(self, filename: str, content: str) -> bool:
        return "rpcclient" in filename.lower() or "enumdomusers" in content

    def parse(self, host: str, content: str, source_file: str):
        creds: List[CredentialFact] = []
        for m in self._USER_RE.finditer(content):
            creds.append(CredentialFact(
                host=host, username=m.group(1).strip(), password="", source_file=source_file
            ))
        access = (
            [AccessFact(host=host, level="read", method="rpcclient", source_file=source_file)]
            if creds else []
        )
        return creds, [], access


class GobusterFfufParser(ITextOutputParser):
    """Parse gobuster / ffuf / dirb / dirsearch web directory scan output."""

    TOOL_NAME = "gobuster"

    # gobuster: /admin                (Status: 200) [Size: 1234]
    _GB_RE   = re.compile(r"^(/\S+)\s+\(Status:\s*(\d+)\)\s+\[Size:\s*(\d+)\]", re.MULTILINE)
    # ffuf:      admin               [Status: 200, Size: 1234,
    _FFUF_RE = re.compile(r"^(\S+)\s+\[Status:\s*(\d+),\s*Size:\s*(\d+)", re.MULTILINE)
    # dirb:  + http://host/admin (CODE:200|SIZE:1234)
    _DIRB_RE = re.compile(r"\+\s+\S+?(/\S+)\s+\(CODE:(\d+)\|SIZE:(\d+)\)")

    def can_parse(self, filename: str, content: str) -> bool:
        return any(
            k in filename.lower()
            for k in ("gobuster", "ffuf", "dirb", "wfuzz", "dirsearch", "ferox")
        )

    def parse(self, host: str, content: str, source_file: str):
        return [], [], []

    def parse_extended(self, host: str, content: str, source_file: str, port: int = 80):
        paths: List[DiscoveredPath] = []
        for m in self._GB_RE.finditer(content):
            paths.append(DiscoveredPath(
                host=host, port=port, path=m.group(1),
                status_code=int(m.group(2)), size=int(m.group(3)),
                source_file=source_file,
            ))
        for m in self._FFUF_RE.finditer(content):
            path = m.group(1)
            if not path.startswith("/"):
                path = "/" + path
            paths.append(DiscoveredPath(
                host=host, port=port, path=path,
                status_code=int(m.group(2)), size=int(m.group(3)),
                source_file=source_file,
            ))
        for m in self._DIRB_RE.finditer(content):
            paths.append(DiscoveredPath(
                host=host, port=port, path=m.group(1),
                status_code=int(m.group(2)), size=int(m.group(3)),
                source_file=source_file,
            ))
        return [], [], [], [], paths


class NiktoParser(ITextOutputParser):
    """Parse nikto web scanner output."""

    TOOL_NAME = "nikto"

    _VULN_RE = re.compile(
        r"\+\s+(OSVDB-\d+|CVE-[\d-]+):\s*(/[^:]*)?:\s*(.+)"
    )
    _PATH_RE = re.compile(r"\+\s+(/\S+):\s+.+\(CODE:(\d+)\|SIZE:(\d+)\)")

    def can_parse(self, filename: str, content: str) -> bool:
        return "nikto" in filename.lower() or "- Nikto v" in content

    def parse(self, host: str, content: str, source_file: str):
        return [], [], []

    def parse_extended(self, host: str, content: str, source_file: str, port: int = 80):
        vulns: List[VulnerabilityFact] = []
        paths: List[DiscoveredPath] = []
        for m in self._VULN_RE.finditer(content):
            vulns.append(VulnerabilityFact(
                host=host,
                vuln_id=m.group(1),
                severity="medium",
                title=m.group(3).strip()[:200],
                url=m.group(2) or "/",
                source_tool="nikto",
                source_file=source_file,
            ))
        for m in self._PATH_RE.finditer(content):
            paths.append(DiscoveredPath(
                host=host, port=port, path=m.group(1),
                status_code=int(m.group(2)), size=int(m.group(3)),
                source_file=source_file,
            ))
        return [], [], [], vulns, paths


class NucleiParser(ITextOutputParser):
    """Parse nuclei scanner output."""

    TOOL_NAME = "nuclei"

    # [severity] [template-id] [protocol] target
    _RE = re.compile(r"\[(\w+)\]\s+\[([^\]]+)\]\s+\[(\w+)\]\s+(\S+)")

    def can_parse(self, filename: str, content: str) -> bool:
        return "nuclei" in filename.lower() or bool(
            re.search(r"\[\w+\]\s+\[\S+\]\s+\[\w+\]\s+https?://", content)
        )

    def parse(self, host: str, content: str, source_file: str):
        return [], [], []

    def parse_extended(self, host: str, content: str, source_file: str, port: int = 80):
        vulns: List[VulnerabilityFact] = []
        sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        for m in self._RE.finditer(content):
            severity, tmpl_id, proto, target = m.groups()
            sev = severity.lower()
            if sev not in sev_order:
                sev = "info"
            vulns.append(VulnerabilityFact(
                host=host,
                vuln_id=tmpl_id,
                severity=sev,
                title=f"{tmpl_id} ({proto})",
                url=target,
                source_tool="nuclei",
                source_file=source_file,
            ))
        return [], [], [], vulns, []


class SslscanParser(ITextOutputParser):
    """Parse sslscan / sslyze SSL/TLS analysis output."""

    TOOL_NAME = "sslscan"

    _WEAK_TLS_RE = re.compile(r"(SSLv\d|TLSv1\.0|TLSv1\.1)\s+enabled", re.IGNORECASE)
    _EXPIRED_RE  = re.compile(r"Not valid after:\s+\S+\s+(\d{4})")

    def can_parse(self, filename: str, content: str) -> bool:
        return any(k in filename.lower() for k in ("sslscan", "sslyze", "ssl_audit", "sslscan"))

    def parse(self, host: str, content: str, source_file: str):
        return [], [], []

    def parse_extended(self, host: str, content: str, source_file: str, port: int = 443):
        vulns: List[VulnerabilityFact] = []
        seen: set = set()
        for m in self._WEAK_TLS_RE.finditer(content):
            proto = m.group(1)
            key = (host, proto)
            if key not in seen:
                seen.add(key)
                vulns.append(VulnerabilityFact(
                    host=host,
                    vuln_id="WEAK-TLS",
                    severity="medium",
                    title=f"Weak protocol enabled: {proto}",
                    url=f"https://{host}:{port}/",
                    source_tool="sslscan",
                    source_file=source_file,
                ))
        for m in self._EXPIRED_RE.finditer(content):
            year = int(m.group(1))
            import datetime as _dt
            if year < _dt.datetime.now().year:
                vulns.append(VulnerabilityFact(
                    host=host,
                    vuln_id="EXPIRED-CERT",
                    severity="medium",
                    title=f"Expired SSL certificate (year {year})",
                    url=f"https://{host}:{port}/",
                    source_tool="sslscan",
                    source_file=source_file,
                ))
        return [], [], [], vulns, []


class GenericOutputParser(ITextOutputParser):
    """Catch-all: mine any text for credential-like patterns."""

    TOOL_NAME = "generic"

    _CRED_RE = re.compile(
        r"(?:password|passwd|pass|pwd)\s*[=:]\s*(?P<pass>\S+)", re.IGNORECASE
    )
    _USER_RE = re.compile(
        r"(?:username|user|login)\s*[=:]\s*(?P<user>\S+)", re.IGNORECASE
    )
    _HASH_RE = re.compile(r"\b(?P<hash>[0-9a-fA-F]{32})\b")
    _SHELL_RE = re.compile(r"(?:root|SYSTEM|NT AUTHORITY)\s*[@#$]", re.IGNORECASE)

    def can_parse(self, filename: str, content: str) -> bool:
        return True

    def parse(self, host: str, content: str, source_file: str):
        creds: List[CredentialFact] = []
        shares: List[ShareFact] = []
        access: List[AccessFact] = []
        users = {m.group("user") for m in self._USER_RE.finditer(content)}
        passwords = {m.group("pass") for m in self._CRED_RE.finditer(content)}
        hashes = {m.group("hash") for m in self._HASH_RE.finditer(content)}
        for u in users:
            for p in passwords:
                creds.append(CredentialFact(
                    host=host, username=u, password=p, source_file=source_file
                ))
        for h in hashes:
            creds.append(CredentialFact(
                host=host, username="", password="", hash_value=h,
                hash_type="MD4/NTLM", source_file=source_file,
            ))
        if self._SHELL_RE.search(content):
            access.append(AccessFact(
                host=host, level="root", method="generic", source_file=source_file
            ))
        return creds, shares, access


# ─── FactStore ────────────────────────────────────────────────────────────────


class FactStore:
    """
    Central structured fact repository.

    Parses nmap XML and tool output files, merges them into a per-host
    data model, and persists everything to sessions/policy_facts.json.

    The file is keyed by host IP: { "10.10.11.78": { ... } }
    """

    def __init__(self, cfg: Optional[Config] = None) -> None:
        self._cfg = cfg or Config.default()
        logging.basicConfig(level=getattr(logging, self._cfg.log_level, logging.WARNING))
        self._log = logging.getLogger(self.__class__.__name__)
        self._xml_parser = INmapXmlParser()
        self._text_parsers: List[ITextOutputParser] = [
            CrackMapExecParser(),
            Enum4linuxParser(),
            SecretsdumpParser(),
            LdapParser(),
            KerbruteParser(),
            RpcclientParser(),
            GobusterFfufParser(),
            NiktoParser(),
            NucleiParser(),
            SslscanParser(),
            GenericOutputParser(),
        ]
        self._data: Dict[str, HostFacts] = {}
        self._load()

    # ── persistence ──────────────────────────────────────────────────────────

    def _load(self) -> None:
        if not self._cfg.facts_file.exists():
            return
        try:
            raw = json.loads(self._cfg.facts_file.read_text())
        except (json.JSONDecodeError, OSError):
            return
        for host, blob in raw.items():
            hf = HostFacts(host=host)
            hf.raw_files = blob.get("raw_files", [])
            for s in blob.get("services", []):
                hf.services.append(ServiceFact(**s))
            for c in blob.get("credentials", []):
                hf.credentials.append(CredentialFact(**c))
            for sh in blob.get("shares", []):
                hf.shares.append(ShareFact(**sh))
            for a in blob.get("access", []):
                hf.access.append(AccessFact(**a))
            for v in blob.get("vulnerabilities", []):
                hf.vulnerabilities.append(VulnerabilityFact(**v))
            for p in blob.get("paths", []):
                hf.paths.append(DiscoveredPath(**p))
            hf.os_hint = blob.get("os_hint", "")
            self._data[host] = hf

    def save(self) -> None:
        out: Dict[str, dict] = {}
        for host, hf in self._data.items():
            out[host] = {
                "services":        [asdict(s) for s in hf.services],
                "credentials":     [asdict(c) for c in hf.credentials],
                "shares":          [asdict(sh) for sh in hf.shares],
                "access":          [asdict(a) for a in hf.access],
                "raw_files":       hf.raw_files,
                "vulnerabilities": [asdict(v) for v in hf.vulnerabilities],
                "paths":           [asdict(p) for p in hf.paths],
                "os_hint":         hf.os_hint,
            }
        self._cfg.facts_file.write_text(json.dumps(out, indent=2))

    # ── update helpers ────────────────────────────────────────────────────────

    def _host(self, ip: str) -> HostFacts:
        if ip not in self._data:
            self._data[ip] = HostFacts(host=ip)
        return self._data[ip]

    def _dedup_services(self, hf: HostFacts) -> None:
        seen: set = set()
        unique: List[ServiceFact] = []
        for s in hf.services:
            key = (s.host, s.port, s.protocol)
            if key not in seen:
                seen.add(key)
                unique.append(s)
        hf.services = unique

    def _dedup_creds(self, hf: HostFacts) -> None:
        seen: set = set()
        unique: List[CredentialFact] = []
        for c in hf.credentials:
            key = (c.host, c.username, c.password, c.hash_value)
            if key not in seen:
                seen.add(key)
                unique.append(c)
        hf.credentials = unique

    def _dedup_vulns(self, hf: HostFacts) -> None:
        seen: set = set()
        unique: List[VulnerabilityFact] = []
        for v in hf.vulnerabilities:
            key = (v.host, v.vuln_id, v.url)
            if key not in seen:
                seen.add(key)
                unique.append(v)
        hf.vulnerabilities = unique

    def _dedup_paths(self, hf: HostFacts) -> None:
        seen: set = set()
        unique: List[DiscoveredPath] = []
        for p in hf.paths:
            key = (p.host, p.port, p.path, p.status_code)
            if key not in seen:
                seen.add(key)
                unique.append(p)
        hf.paths = unique

    # ── parsers ───────────────────────────────────────────────────────────────

    def ingest_xml(self, xml_path: Path) -> int:
        """Parse one nmap XML file, merge results, return count of new facts."""
        facts = self._xml_parser.parse(xml_path)
        count = 0
        for sf in facts:
            hf = self._host(sf.host)
            hf.services.append(sf)
            count += 1
        for hf in self._data.values():
            self._dedup_services(hf)
        return count

    def ingest_text(self, txt_path: Path, host_hint: str = "") -> int:
        """Parse one tool output file, merge credential/share/access facts."""
        try:
            content = txt_path.read_text(errors="replace")
        except OSError:
            return 0
        if not content.strip():
            return 0

        filename = txt_path.name
        host = host_hint or self._guess_host_from_filename(filename)
        if not host:
            return 0

        count = 0
        port = self._guess_port_from_path(txt_path)
        for parser in self._text_parsers:
            if parser.can_parse(filename, content):
                creds, shares, access, vulns, paths = parser.parse_extended(
                    host, content, source_file=str(txt_path), port=port
                )
                hf = self._host(host)
                if str(txt_path) not in hf.raw_files:
                    hf.raw_files.append(str(txt_path))
                hf.credentials.extend(creds)
                hf.shares.extend(shares)
                hf.access.extend(access)
                hf.vulnerabilities.extend(vulns)
                hf.paths.extend(paths)
                self._dedup_creds(hf)
                self._dedup_vulns(hf)
                self._dedup_paths(hf)
                count += len(creds) + len(shares) + len(access) + len(vulns) + len(paths)
                if parser.TOOL_NAME != "generic":
                    break
        return count

    @staticmethod
    def _guess_host_from_filename(filename: str) -> str:
        """Try to extract an IP from a filename like 10.10.11.78_enum_smb.txt."""
        m = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", filename)
        return m.group(1) if m else ""

    @staticmethod
    def _guess_port_from_path(txt_path: Path) -> int:
        """Extract port from sessions/<ip>/<port>/<tool>/ directory structure."""
        parts = txt_path.parts
        try:
            sessions_idx = next(i for i, p in enumerate(parts) if p == "sessions")
            port_candidate = parts[sessions_idx + 2]
            return int(port_candidate)
        except (StopIteration, IndexError, ValueError):
            return 80

    # ── full scan ─────────────────────────────────────────────────────────────

    def parse_all(self, target: Optional[str] = None) -> Dict[str, int]:
        """
        Scan sessions/ for all nmap XML and txt files.

        If target is given only process files that appear to belong to that IP.
        Returns a dict of {host: new_facts_count}.
        """
        counts: Dict[str, int] = {}

        for xml_path in self._cfg.sessions_dir.glob(self._cfg.xml_glob):
            if target and target not in xml_path.name:
                continue
            n = self.ingest_xml(xml_path)
            counts["_xml"] = counts.get("_xml", 0) + n

        for txt_path in self._cfg.sessions_dir.glob(self._cfg.txt_glob):
            if target and target not in txt_path.name:
                host_hint = target
            else:
                host_hint = self._guess_host_from_filename(txt_path.name)
                if target and host_hint != target:
                    continue
            n = self.ingest_text(txt_path, host_hint)
            host = host_hint or "unknown"
            counts[host] = counts.get(host, 0) + n

        self.save()
        return counts

    # ── query API ─────────────────────────────────────────────────────────────

    def get_host(self, host: str) -> Optional[HostFacts]:
        return self._data.get(host)

    def all_hosts(self) -> List[str]:
        return sorted(self._data.keys())

    def context_for_command(self, host: str, category: str) -> Dict[str, object]:
        """
        Return a dict of substitution parameters for a command in the given
        attack category.  The auto_loop uses these to build concrete commands.

        Returned keys (may be empty strings if unknown):
            port, service, username, password, hash, shares, domain
        """
        hf = self._data.get(host)
        if hf is None:
            return {}

        ctx: Dict[str, object] = {"host": host}

        # Pick best port/service for the category
        port_pref: Dict[str, List[str]] = {
            "enum":       ["smb", "microsoft-ds", "netbios-ssn", "ldap", "http", "ftp"],
            "brute_force":["ssh", "rdp", "ftp", "telnet", "smb", "microsoft-ds"],
            "exploit":    ["http", "https", "smb", "microsoft-ds", "ftp", "ssh"],
            "intrusion":  ["winrm", "rdp", "ssh", "telnet"],
            "privesc":    [],
            "credential": ["smb", "microsoft-ds", "ldap"],
            "lateral":    ["smb", "microsoft-ds", "winrm", "rdp"],
        }
        preferred = port_pref.get(category, [])
        chosen_svc: Optional[ServiceFact] = None
        for svc_name in preferred:
            matches = hf.services_by_name(svc_name)
            if matches:
                chosen_svc = matches[0]
                break
        if chosen_svc is None and hf.services:
            chosen_svc = hf.services[0]
        if chosen_svc:
            ctx["port"] = chosen_svc.port
            ctx["service"] = chosen_svc.service

        # Best credential
        creds_with_pass = [c for c in hf.credentials if c.password]
        creds_with_hash = [c for c in hf.credentials if c.hash_value]
        if creds_with_pass:
            c = creds_with_pass[0]
            ctx["username"] = c.username
            ctx["password"] = c.password
        elif creds_with_hash:
            c = creds_with_hash[0]
            ctx["username"] = c.username
            ctx["hash"] = c.hash_value
            ctx["password"] = ""
        else:
            # Fall back to any username from enumeration
            usernames = [c.username for c in hf.credentials if c.username]
            ctx["username"] = usernames[0] if usernames else ""
            ctx["password"] = ""

        # Shares
        if hf.shares:
            ctx["shares"] = [s.share_name for s in hf.shares]
        else:
            ctx["shares"] = []

        # Access level
        ctx["access_level"] = hf.highest_access()
        ctx["open_ports"] = hf.open_ports()

        # Vulnerabilities — most severe first
        if hf.vulnerabilities:
            sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
            sorted_vulns = sorted(
                hf.vulnerabilities,
                key=lambda v: sev_order.get(v.severity, 5),
            )
            ctx["top_vuln"] = {
                "id":       sorted_vulns[0].vuln_id,
                "severity": sorted_vulns[0].severity,
                "title":    sorted_vulns[0].title,
            }
            ctx["vuln_count"] = len(hf.vulnerabilities)
        else:
            ctx["top_vuln"] = None
            ctx["vuln_count"] = 0

        # Discovered web paths
        if hf.paths:
            ctx["interesting_paths"] = [
                p.path for p in hf.paths
                if p.status_code in (200, 201, 301, 302, 401, 403)
            ][:5]
        else:
            ctx["interesting_paths"] = []

        return ctx

    def summary(self, host: Optional[str] = None) -> str:
        """Return a human-readable summary of stored facts."""
        hosts = [host] if host else self.all_hosts()
        if not hosts:
            return "No facts stored yet. Run parse_all() first."
        lines: List[str] = []
        for h in hosts:
            hf = self._data.get(h)
            if not hf:
                lines.append(f"{h}: no data")
                continue
            ports = hf.open_ports()
            svcs = ", ".join(sorted({s.service for s in hf.services if s.service})) or "?"
            cred_count = len([c for c in hf.credentials if c.username])
            share_count = len(hf.shares)
            access = hf.highest_access()
            vuln_count = len(hf.vulnerabilities)
            path_count = len(hf.paths)
            lines.append(
                f"{h}  ports={ports}  services=[{svcs}]  "
                f"creds={cred_count}  shares={share_count}  "
                f"vulns={vuln_count}  paths={path_count}  access={access}"
            )
        return "\n".join(lines)


# ─── Tool file factory ────────────────────────────────────────────────────────


@dataclass
class ToolDefinition:
    """A pwntomate .tool file definition."""

    toolname: str
    command: str
    trigger: List[str]
    active: bool = True


def create_tool_file(
    toolname: str,
    command: str,
    trigger: List[str],
    active: bool = True,
    tools_dir: Optional[Path] = None,
) -> Path:
    """
    Write a new pwntomate .tool JSON file.

    Sanitises the toolname for the filesystem (spaces → underscores).
    Returns the path written.
    """
    if tools_dir is None:
        tools_dir = Path(__file__).parent.parent / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^\w\-]", "_", toolname).strip("_").lower()
    out_path = tools_dir / f"{safe_name}.tool"
    defn = ToolDefinition(toolname=toolname, command=command, trigger=trigger, active=active)
    out_path.write_text(json.dumps(asdict(defn), indent=4))
    return out_path


# ─── CLI ─────────────────────────────────────────────────────────────────────


def _cmd_parse(args: argparse.Namespace) -> None:
    store = FactStore()
    counts = store.parse_all(target=args.target)
    total = sum(v for k, v in counts.items() if not k.startswith("_xml"))
    xml_total = counts.get("_xml", 0)
    print(f"Parsed {xml_total} service facts from XML, {total} text facts from tool output.")
    print(store.summary(args.target))


def _cmd_show(args: argparse.Namespace) -> None:
    store = FactStore()
    print(store.summary(args.target))


def _cmd_clean(_args: argparse.Namespace) -> None:
    cfg = Config.default()
    if cfg.facts_file.exists():
        cfg.facts_file.unlink()
        print(f"Deleted {cfg.facts_file}")
    else:
        print("Nothing to clean.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LazyOwn FactStore — structured fact extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_parse = sub.add_parser("parse", help="Ingest all XML and txt files in sessions/")
    p_parse.add_argument("--target", default=None, help="Filter to a specific target IP")

    p_show = sub.add_parser("show", help="Print stored facts")
    p_show.add_argument("--target", default=None, help="Filter to a specific target IP")

    sub.add_parser("clean", help="Delete sessions/policy_facts.json")

    args = parser.parse_args()
    if args.cmd == "parse":
        _cmd_parse(args)
    elif args.cmd == "show":
        _cmd_show(args)
    elif args.cmd == "clean":
        _cmd_clean(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

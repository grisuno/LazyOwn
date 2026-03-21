#!/usr/bin/env python3
"""
modules/obs_parser.py
======================
Observation parser: extracts structured findings from raw tool output.

Converts unstructured text (nmap, gobuster, crackmapexec, enum4linux, etc.)
into typed Finding objects that the WorldModel can ingest directly.

Extractors are independent, additive, and follow Open/Closed:
  - Add a new extractor by subclassing Extractor and registering it.
  - Existing extractors are never modified to support new patterns.

Design
------
- Single Responsibility : each Extractor owns one finding type
- Open/Closed           : new types via new Extractor subclass
- Liskov                : all Extractor subclasses honour the same contract
- Interface Segregation : consumers only see FindingType, Finding, Observation
- Dependency Inversion  : ObsParser depends on Extractor abstraction

Usage
-----
    from modules.obs_parser import ObsParser

    parser = ObsParser()
    obs    = parser.parse(nmap_output, host="10.10.11.78", tool="nmap")

    for finding in obs.findings:
        print(finding.type, finding.value, finding.confidence)
"""
from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

log = logging.getLogger("obs_parser")


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

class FindingType(str, Enum):
    IP              = "ip"
    CREDENTIAL      = "credential"
    SERVICE_VERSION = "service_version"
    PATH            = "path"
    USERNAME        = "username"
    HASH            = "hash"
    CVE             = "cve"
    DOMAIN          = "domain"
    EMAIL           = "email"
    ERROR           = "error"


@dataclass
class Finding:
    type:       FindingType
    value:      str
    host:       str   = ""
    confidence: float = 1.0
    raw:        str   = ""


@dataclass
class Observation:
    findings:   List[Finding] = field(default_factory=list)
    tool:       str           = ""
    host:       str           = ""
    raw_output: str           = ""
    success:    bool          = True

    def by_type(self, ftype: FindingType) -> List[Finding]:
        return [f for f in self.findings if f.type == ftype]

    def has(self, ftype: FindingType) -> bool:
        return any(f.type == ftype for f in self.findings)


# ---------------------------------------------------------------------------
# Extractor base and registry
# ---------------------------------------------------------------------------

class Extractor(ABC):
    """Base class for a single finding-type extractor."""

    @abstractmethod
    def extract(self, text: str, host: str) -> List[Finding]:
        """Return all findings of this type found in *text*."""


class _ExtractorRegistry:
    """Holds the ordered list of active Extractor instances."""

    def __init__(self) -> None:
        self._extractors: List[Extractor] = []

    def register(self, extractor: Extractor) -> None:
        self._extractors.append(extractor)

    def run_all(self, text: str, host: str) -> List[Finding]:
        findings: List[Finding] = []
        for ext in self._extractors:
            try:
                findings.extend(ext.extract(text, host))
            except Exception as exc:
                log.debug("Extractor %s failed: %s", type(ext).__name__, exc)
        return findings


# ---------------------------------------------------------------------------
# Concrete extractors
# ---------------------------------------------------------------------------

class _IPExtractor(Extractor):
    _PATTERN = re.compile(
        r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
        r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b'
    )
    _EXCLUDE = {"0.0.0.0", "255.255.255.255", "127.0.0.1"}

    def extract(self, text: str, host: str) -> List[Finding]:
        seen: set = set()
        results: List[Finding] = []
        for m in self._PATTERN.finditer(text):
            ip = m.group()
            if ip not in seen and ip not in self._EXCLUDE and ip != host:
                seen.add(ip)
                results.append(Finding(FindingType.IP, ip, host=host, confidence=0.9))
        return results


class _CredentialExtractor(Extractor):
    """Matches user:password patterns from tool output."""
    _PATTERNS = [
        # crackmapexec / netexec style
        re.compile(r'(?i)\[\+\]\s+[\w.@-]+\\([\w.@-]+):([\S]+)'),
        # secretsdump style
        re.compile(r'([\w.@-]+):([\w.@-]+):([0-9a-f]{32}):([0-9a-f]{32}):::', re.IGNORECASE),
        # generic user:pass
        re.compile(r'\b([\w.@-]{2,30}):([\S]{4,100})\b'),
    ]
    _MIN_PASSWORD_LEN = 4
    _SKIP_WORDS = {"etc", "passwd", "shadow", "group", "var", "tmp", "usr",
                   "bin", "lib", "sys", "dev", "proc", "run", "opt", "srv"}

    def extract(self, text: str, host: str) -> List[Finding]:
        seen: set = set()
        results: List[Finding] = []
        for pat in self._PATTERNS:
            for m in pat.finditer(text):
                username = m.group(1)
                password = m.group(2)
                if username.lower() in self._SKIP_WORDS:
                    continue
                if len(password) < self._MIN_PASSWORD_LEN:
                    continue
                cred = f"{username}:{password}"
                if cred not in seen:
                    seen.add(cred)
                    results.append(Finding(
                        FindingType.CREDENTIAL, cred,
                        host=host, confidence=0.8, raw=m.group()
                    ))
        return results


class _ServiceVersionExtractor(Extractor):
    """Extracts service name + version from nmap-style output."""
    _PATTERN = re.compile(
        r'(\d+)/(?:tcp|udp)\s+open\s+([\w/-]+)(?:\s+([\w/. -]+))?'
    )

    def extract(self, text: str, host: str) -> List[Finding]:
        results: List[Finding] = []
        for m in self._PATTERN.finditer(text):
            name    = m.group(2).strip()
            version = (m.group(3) or "").strip()
            value   = f"{name} {version}".strip()
            results.append(Finding(
                FindingType.SERVICE_VERSION, value,
                host=host, confidence=0.95, raw=m.group()
            ))
        return results


class _PathExtractor(Extractor):
    """Extracts URL paths from gobuster / ffuf / nikto output."""
    _PATTERN = re.compile(r'(?:Found|Status).*?(\/[\w/._-]{2,100})')

    def extract(self, text: str, host: str) -> List[Finding]:
        seen: set = set()
        results: List[Finding] = []
        for m in self._PATTERN.finditer(text):
            path = m.group(1)
            if path not in seen:
                seen.add(path)
                results.append(Finding(FindingType.PATH, path, host=host, confidence=0.85))
        return results


class _UsernameExtractor(Extractor):
    """Extracts usernames from enum4linux / kerbrute / rpcclient output."""
    _PATTERNS = [
        re.compile(r'(?i)user:\s*([\w.@-]+)'),
        re.compile(r'(?i)\[\\+\]\s+([\w.@-]+)\s+is valid'),
        re.compile(r'(?i)account:\s*([\w.@-]+)'),
        re.compile(r'RID\s+\d+.*?\\([\w.@-]+)'),
    ]

    def extract(self, text: str, host: str) -> List[Finding]:
        seen: set = set()
        results: List[Finding] = []
        for pat in self._PATTERNS:
            for m in pat.finditer(text):
                user = m.group(1).strip()
                if user and user not in seen and len(user) < 64:
                    seen.add(user)
                    results.append(Finding(
                        FindingType.USERNAME, user,
                        host=host, confidence=0.85, raw=m.group()
                    ))
        return results


class _HashExtractor(Extractor):
    """Extracts NTLM and other hashes from tool output."""
    _PATTERNS = [
        # NTLM from secretsdump: user:RID:LM:NTLM:::
        re.compile(r'([\w.@-]+):\d+:[0-9a-f]{32}:([0-9a-f]{32}):::', re.IGNORECASE),
        # Standalone 32-char MD5/NTLM
        re.compile(r'\b([0-9a-f]{32})\b', re.IGNORECASE),
        # SHA-256
        re.compile(r'\b([0-9a-f]{64})\b', re.IGNORECASE),
        # bcrypt
        re.compile(r'(\$2[aby]?\$\d+\$[\w./+]{53})'),
    ]

    def extract(self, text: str, host: str) -> List[Finding]:
        seen: set = set()
        results: List[Finding] = []
        for pat in self._PATTERNS:
            for m in pat.finditer(text):
                h = m.group(1) if m.lastindex == 1 else m.group(2)
                if h and h not in seen:
                    seen.add(h)
                    results.append(Finding(
                        FindingType.HASH, h,
                        host=host, confidence=0.9, raw=m.group()
                    ))
        return results


class _CVEExtractor(Extractor):
    """Extracts CVE identifiers from any output."""
    _PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)

    def extract(self, text: str, host: str) -> List[Finding]:
        seen: set = set()
        results: List[Finding] = []
        for m in self._PATTERN.finditer(text):
            cve = m.group().upper()
            if cve not in seen:
                seen.add(cve)
                results.append(Finding(FindingType.CVE, cve, host=host, confidence=1.0))
        return results


class _DomainExtractor(Extractor):
    """Extracts hostnames and domain names."""
    _PATTERN = re.compile(
        r'\b((?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,})\b'
    )
    _SKIP_TLDS = {".py", ".txt", ".log", ".xml", ".json", ".sh", ".md"}

    def extract(self, text: str, host: str) -> List[Finding]:
        seen: set = set()
        results: List[Finding] = []
        for m in self._PATTERN.finditer(text):
            domain = m.group(1).lower()
            if any(domain.endswith(t) for t in self._SKIP_TLDS):
                continue
            if domain not in seen:
                seen.add(domain)
                results.append(Finding(
                    FindingType.DOMAIN, domain,
                    host=host, confidence=0.7
                ))
        return results


class _ErrorExtractor(Extractor):
    """Detects error / failure indicators in output."""
    _PATTERNS = [
        re.compile(r'(?i)(connection refused|timed? out|no route to host|access denied|'
                   r'permission denied|authentication fail|invalid credential|'
                   r'host unreachable)'),
    ]

    def extract(self, text: str, host: str) -> List[Finding]:
        results: List[Finding] = []
        for pat in self._PATTERNS:
            m = pat.search(text)
            if m:
                results.append(Finding(
                    FindingType.ERROR, m.group(1).lower(),
                    host=host, confidence=0.9, raw=m.group()
                ))
                break  # one error marker is enough
        return results


# ---------------------------------------------------------------------------
# Success heuristic
# ---------------------------------------------------------------------------

class _SuccessDetector:
    """
    Heuristic: decide whether a tool output represents a successful execution.
    Not a precise classifier — supplements the policy engine rather than replacing it.
    """
    _FAILURE_PATTERNS = re.compile(
        r'(?i)(error|exception|failed|traceback|not found|'
        r'connection refused|timed? out|no such file)',
        re.IGNORECASE,
    )
    _SUCCESS_PATTERNS = re.compile(
        r'(?i)(open|found|success|completed|running|active|'
        r'listening|authenticated|\[\+\])',
        re.IGNORECASE,
    )

    def is_success(self, text: str) -> bool:
        text_l = text[:2000]
        has_failure = bool(self._FAILURE_PATTERNS.search(text_l))
        has_success = bool(self._SUCCESS_PATTERNS.search(text_l))
        if has_success and not has_failure:
            return True
        if has_failure and not has_success:
            return False
        return len(text.strip()) > 10  # non-empty output = partial success


# ---------------------------------------------------------------------------
# ObsParser
# ---------------------------------------------------------------------------

class ObsParser:
    """
    Parses raw tool output into an Observation containing typed Findings.

    Each registered Extractor runs independently. The order does not matter.
    New extractors can be added via ObsParser.register(extractor).
    """

    def __init__(self) -> None:
        self._registry = _ExtractorRegistry()
        self._success  = _SuccessDetector()
        # Register default extractors
        for ext in [
            _ServiceVersionExtractor(),
            _IPExtractor(),
            _CredentialExtractor(),
            _HashExtractor(),
            _CVEExtractor(),
            _PathExtractor(),
            _UsernameExtractor(),
            _DomainExtractor(),
            _ErrorExtractor(),
        ]:
            self._registry.register(ext)

    def register(self, extractor: Extractor) -> None:
        """Register an additional Extractor (Open/Closed extension point)."""
        self._registry.register(extractor)

    def parse(self, output: str, host: str = "", tool: str = "") -> Observation:
        """
        Parse *output* and return an Observation.

        Parameters
        ----------
        output : raw text from a tool (nmap, gobuster, enum4linux, etc.)
        host   : IP or hostname the tool was run against
        tool   : tool name (for context only — does not affect extraction)
        """
        if not output or not output.strip():
            return Observation(tool=tool, host=host, raw_output=output, success=False)

        findings = self._registry.run_all(output, host)
        success  = self._success.is_success(output)

        # Dedup: same type + value combination
        seen:   set          = set()
        unique: List[Finding] = []
        for f in findings:
            key = (f.type, f.value)
            if key not in seen:
                seen.add(key)
                unique.append(f)

        log.debug(
            "ObsParser: tool=%s host=%s findings=%d success=%s",
            tool, host, len(unique), success,
        )
        return Observation(
            findings   = unique,
            tool       = tool,
            host       = host,
            raw_output = output,
            success    = success,
        )


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_parser: Optional[ObsParser] = None


def get_parser() -> ObsParser:
    """Return (or create) the module-level singleton ObsParser."""
    global _default_parser
    if _default_parser is None:
        _default_parser = ObsParser()
    return _default_parser


def parse(output: str, host: str = "", tool: str = "") -> Observation:
    """Module-level convenience wrapper."""
    return get_parser().parse(output, host=host, tool=tool)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    p = argparse.ArgumentParser(description="LazyOwn Observation Parser")
    p.add_argument("--file", help="Read tool output from file (else read stdin)")
    p.add_argument("--host", default="", help="Target host the tool ran against")
    p.add_argument("--tool", default="", help="Tool name (for labelling)")
    args = p.parse_args()

    if args.file:
        text = open(args.file, "r", encoding="utf-8", errors="replace").read()
    else:
        text = sys.stdin.read()

    obs = parse(text, host=args.host, tool=args.tool)
    print(f"Success: {obs.success}   Findings: {len(obs.findings)}")
    print()
    for f in obs.findings:
        print(f"  [{f.type.value:16s}] conf={f.confidence:.2f}  {f.value[:100]}")

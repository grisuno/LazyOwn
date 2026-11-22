"""Declared finding class and typed evidence predicates.

Ports the outcome taxonomy of :mod:`modules.exploit_engine.outcomes` to
the loop finding lifecycle. Two rules:

* a finding's class comes from its declared metadata (technique id,
  vulnclass) — never from output keywords alone, so a T1005 collection
  test can never be reported as SQLi because the word "SQL" appeared in
  a SQLite dump;
* a retest may only confirm a finding when the captured evidence
  satisfies the class's differential predicate — a ``200`` banner, a
  generic ``vulnerable`` string or a quoted line that carries no typed
  signal never proves anything.

Pure functions only; every predicate fails open for unknown classes so
the loop keeps working while the vocabulary grows.
"""

from __future__ import annotations

import re

_SHELL_PROOF_RE = re.compile(r"uid=\d+\(\w+\)|nt authority\\system|root shell|shell obtained|# ", re.IGNORECASE)
_FILE_PROOF_RE = re.compile(
    r"^(?:root|daemon|bin|sys|sync|games|man|lp|mail|news|uucp|proxy|www-data|backup|list|"
    r"irc|gnats|nobody|libuuid|dhcp|syslog|klog|sshd|msfadmin|postgres|mysql|tomcat55|"
    r"distccd|user|service|telnet|proftpd|statd|snmp|art):[^:\n]*:\d+:\d+:",
    re.MULTILINE,
)
_SHADOW_PROOF_RE = re.compile(r"^[^:\n]+:\$[0-9a-zA-Z]+\$[^\n]*:", re.MULTILINE)
_SQLI_PROOF_RE = re.compile(
    r"You have an error in your SQL syntax|Warning:\s*mysql_|SQLSTATE\[|"
    r"syntax error at or near|ORA-\d{4,5}|PostgreSQL.*ERROR",
    re.IGNORECASE,
)
_XSS_PROOF_RE = re.compile(r"<script[^>]*>.*?</script>|alert\(\s*1\s*\)|XSS_EXECUTED", re.IGNORECASE)
_ANON_PROOF_RE = re.compile(
    r"230[ -](?:Anonymous access granted|Login successful)|Anonymous login successful", re.IGNORECASE
)
_BYPASS_PROOF_RE = re.compile(
    r"Welcome to phpMyAdmin|You have logged in|Logged in as|Login successful|"
    r"Authentication succeeded|Successfully logged in",
    re.IGNORECASE,
)
_CRED_PROOF_RE = re.compile(
    r"(?:database|db|mysql|postgres|ftp|ssh|admin|root)?\s*password\s+"
    r"(?:is\s+set\s+to|[:=])\s*\S+|"
    r"DB_(?:PASSWORD|PASS|PWD)\s*[:=]\s*\S+",
    re.IGNORECASE,
)
_BRUTE_PROOF_RE = re.compile(r"valid password found|\[\d+\]\[[^\]]+\]\s+host:", re.IGNORECASE)
_COLLECTION_PROOF_RE = re.compile(
    r"^(?:root|daemon|bin|sys|nobody|www-data|msfadmin):[^:\n]*:\d+:\d+:|^\s*\d+\s*\|\s*\S+\s*\|",
    re.MULTILINE,
)

FILE_READ = "file_read"
COLLECTION = "collection"
SHELL = "shell"
SQLI = "sqli"
XSS = "xss"
ANON_ACCESS = "anon_access"
AUTH_BYPASS = "auth_bypass"
CREDENTIAL_LEAK = "credential_leak"
CREDENTIAL_UNVERIFIED = "credential_unverified"

TECHNIQUE_CLASSES: dict[str, str] = {
    "T1005": COLLECTION,
    "T1083": FILE_READ,
    "T1087": COLLECTION,
    "T1059": SHELL,
    "T1059.001": SHELL,
    "T1059.007": XSS,
    "T1190": AUTH_BYPASS,
    "T1110": CREDENTIAL_UNVERIFIED,
    "T1552": CREDENTIAL_LEAK,
    "T1555": CREDENTIAL_LEAK,
    "T1003": CREDENTIAL_LEAK,
    "T1003.003": CREDENTIAL_LEAK,
    "T1078": AUTH_BYPASS,
    "T1210": ANON_ACCESS,
    "T1021": SHELL,
    "T1505.003": SHELL,
    "T1548": SHELL,
    "T1548.001": SHELL,
    "T1548.003": SHELL,
    "T1068": SHELL,
}

VULNCLASS_CLASSES: dict[str, str] = {
    "sqli": SQLI,
    "xss": XSS,
    "lfi": FILE_READ,
    "rfi": FILE_READ,
    "file_read": FILE_READ,
    "collection": COLLECTION,
    "rce": SHELL,
    "ssti": SHELL,
    "shell": SHELL,
    "privesc": SHELL,
    "suid": SHELL,
    "sudo": SHELL,
    "kernel": SHELL,
    "brute": CREDENTIAL_UNVERIFIED,
    "bruteforce": CREDENTIAL_UNVERIFIED,
    "spray": CREDENTIAL_UNVERIFIED,
    "credentials": CREDENTIAL_LEAK,
    "credential_dump": CREDENTIAL_LEAK,
    "password": CREDENTIAL_LEAK,
    "mimikatz": CREDENTIAL_LEAK,
    "creds": CREDENTIAL_LEAK,
    "defaults": AUTH_BYPASS,
    "valid_accounts": AUTH_BYPASS,
    "anon": ANON_ACCESS,
    "anonymous": ANON_ACCESS,
    "null_session": ANON_ACCESS,
}

_SHELL_CLASSES = frozenset({SHELL})
_FILE_CLASSES = frozenset({FILE_READ, COLLECTION})

_PREDICATES: dict[str, object] = {}
_PREDICATES[SHELL] = lambda text: _SHELL_PROOF_RE.search(text)
_PREDICATES[FILE_READ] = lambda text: _FILE_PROOF_RE.search(text) or _SHADOW_PROOF_RE.search(text)
_PREDICATES[COLLECTION] = lambda text: (
    _COLLECTION_PROOF_RE.search(text) or _FILE_PROOF_RE.search(text) or _SHADOW_PROOF_RE.search(text)
)
_PREDICATES[SQLI] = lambda text: _SQLI_PROOF_RE.search(text)
_PREDICATES[XSS] = lambda text: _XSS_PROOF_RE.search(text)
_PREDICATES[ANON_ACCESS] = lambda text: _ANON_PROOF_RE.search(text)
_PREDICATES[AUTH_BYPASS] = lambda text: _BYPASS_PROOF_RE.search(text)
_PREDICATES[CREDENTIAL_LEAK] = lambda text: _CRED_PROOF_RE.search(text)
_PREDICATES[CREDENTIAL_UNVERIFIED] = lambda text: _BRUTE_PROOF_RE.search(text)


def class_for_finding(meta: dict | None = None, text: str = "") -> str:
    """Resolve the declared outcome class for one finding.

    Priority: vulnclass from metadata (the declared intent), then the
    technique id from metadata, then a technique id quoted in the finding
    text itself. Bare text keywords are never consulted, so class cannot
    drift with output wording.

    Args:
        meta: Finding metadata (``technique_id``, ``vulnclass``).
        text: Finding text scanned for an embedded technique id.

    Returns:
        The outcome class slug, or "" when the finding carries no
        declared class.
    """
    data = meta or {}
    vulnclass = str(data.get("vulnclass", "") or "").strip().lower()
    if vulnclass and vulnclass in VULNCLASS_CLASSES:
        return VULNCLASS_CLASSES[vulnclass]
    technique = str(data.get("technique_id", "") or "").strip().upper()
    if technique:
        base = technique.split(".", 1)[0]
        if technique in TECHNIQUE_CLASSES:
            return TECHNIQUE_CLASSES[technique]
        if base in TECHNIQUE_CLASSES:
            return TECHNIQUE_CLASSES[base]
    match = re.search(r"\bT(\d{4}(?:\.\d{3})?)\b", str(text or ""))
    if match:
        technique = f"T{match.group(1)}"
        if technique in TECHNIQUE_CLASSES:
            return TECHNIQUE_CLASSES[technique]
    return ""


def evidence_supports_class(class_name: str, evidence_text: str) -> bool:
    """Return True when captured evidence proves the declared class.

    Args:
        class_name: Outcome class slug from :func:`class_for_finding`.
        evidence_text: Captured output under retest.

    Returns:
        True when a differential predicate for the class fires. Unknown
        classes fail open (True) so untyped findings keep the legacy
        verdict path.
    """
    predicate = _PREDICATES.get(str(class_name or ""))
    if predicate is None:
        return True
    try:
        return bool(predicate(str(evidence_text or "")))
    except Exception:
        return True


__all__ = [
    "AUTH_BYPASS",
    "ANON_ACCESS",
    "COLLECTION",
    "CREDENTIAL_LEAK",
    "CREDENTIAL_UNVERIFIED",
    "FILE_READ",
    "SHELL",
    "SQLI",
    "TECHNIQUE_CLASSES",
    "VULNCLASS_CLASSES",
    "XSS",
    "class_for_finding",
    "evidence_supports_class",
]

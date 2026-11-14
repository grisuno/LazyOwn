"""Service alias knowledge for the matching surfaces.

One home for the alias tables consumed by the exploit chain (canonical
group expansion), the chain family normalizer (alias to canonical) and
the auto-registry trigger matcher (symmetric alias pairs). The three
views have different semantics and are kept as distinct named tables so
each consumer's matching behavior is unchanged while the knowledge
cannot drift between files.
"""

from __future__ import annotations

CANONICAL_SERVICE_ALIASES: dict[str, list[str]] = {
    "smb": ["smb", "microsoft-ds", "netbios-ssn", "cifs"],
    "ssh": ["ssh", "ssh-alt"],
    "http": ["http", "https", "http-alt", "http-proxy", "www"],
    "mysql": ["mysql", "mysql-alt"],
    "ftp": ["ftp", "ftp-alt", "ftp-data"],
    "redis": ["redis", "redis-alt"],
    "rpc": ["rpc", "msrpc", "rpcbind", "netbios-ns"],
    "ollama": ["ollama"],
    "node.js": [],
    "golang": [],
}

ALIAS_TO_CANONICAL: dict[str, str] = {
    "www": "http",
    "http-alt": "http",
    "https-alt": "https",
    "microsoft-ds": "smb",
    "netbios-ssn": "smb",
    "ms-wbt-server": "rdp",
}

ALIAS_PAIRS: dict[str, tuple[str, ...]] = {
    "ssl": ("https",),
    "https": ("ssl",),
    "microsoft-ds": ("smb",),
    "smb": ("microsoft-ds", "netbios-ssn"),
    "netbios-ssn": ("smb",),
}

__all__ = ["ALIAS_PAIRS", "ALIAS_TO_CANONICAL", "CANONICAL_SERVICE_ALIASES"]

"""Lazy saved-search grammar over the engagement database.

A Shodan-lite query language over :mod:`modules.db`: ``key:value`` clamps
with ``-key:value`` exclusions and bare free words, all AND-combined:

    port:3389 -host:vpn tech:"apache tomcat" sev:high

Spot keys (aliases included): ``host``/``ip``, ``port``, ``service``,
``product``/``tech``, ``version``, ``os``, ``state``, ``sev``/``severity``,
``cve``, ``user``. Untagged words search host address, service name,
product text and vulnerability name together.

Rows come from the workspace's hosts/services/vulns/creds through the
public ``LazyOwnDB`` API, so permissions and the workspace contract stay
inside the database layer.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field

from modules.db import LazyOwnDB

KEY_HOST = "host"
KEY_PORT = "port"
KEY_SERVICE = "service"
KEY_PRODUCT = "product"
KEY_VERSION = "version"
KEY_OS = "os"
KEY_STATE = "state"
KEY_SEVERITY = "severity"
KEY_CVE = "cve"
KEY_USER = "user"

KEY_ALIASES = {
    "ip": KEY_HOST,
    "host": KEY_HOST,
    "port": KEY_PORT,
    "svc": KEY_SERVICE,
    "service": KEY_SERVICE,
    "product": KEY_PRODUCT,
    "tech": KEY_PRODUCT,
    "version": KEY_VERSION,
    "os": KEY_OS,
    "state": KEY_STATE,
    "sev": KEY_SEVERITY,
    "severity": KEY_SEVERITY,
    "cve": KEY_CVE,
    "user": KEY_USER,
}

SEVERITY_SYNONYMS = {
    "crit": "critical",
    "critical": "critical",
    "hi": "high",
    "high": "high",
    "med": "medium",
    "medium": "medium",
    "low": "low",
}


@dataclass
class SearchTerm:
    """One comparison clamp from the grammar.

    Attributes:
        key: Spot-key name (post-alias resolution) or empty for free text.
        value: Lowercased comparison value.
        negate: True when the term must NOT match.
    """

    key: str = ""
    value: str = ""
    negate: bool = False


@dataclass
class Query:
    """A parsed search expression.

    Attributes:
        terms: Spot-key clamps.
        free: Bare words matching any searchable text column.
        errors: Parse problems when the grammar was violated.
    """

    terms: list[SearchTerm] = field(default_factory=list)
    free: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def parse(query: str) -> Query:
    """Parse the grammar tokens.

    Args:
        query: Raw query line, e.g. ``port:3389 -host:vpn tech:"apache"``.

    Returns:
        A :class:`Query`; unknown spot keys become ``errors`` entries and
        the term is dropped, so a typo never silently changes the answer.
    """
    parsed = Query()
    try:
        tokens = shlex.split(query or "")
    except ValueError as exc:
        parsed.errors.append(f"bad quote balance: {exc}")
        return parsed
    for token in tokens:
        negate = token.startswith("-")
        if negate:
            token = token[1:]
        if ":" in token:
            key, _, value = token.partition(":")
            key = key.strip().lower()
            value = value.strip().lower()
            if key not in KEY_ALIASES:
                parsed.errors.append(f"unknown spot key: {key}")
                continue
            key = KEY_ALIASES[key]
            value = _canon(key, value)
            if not value:
                parsed.errors.append(f"empty value for {key}:")
                continue
            parsed.terms.append(SearchTerm(key=key, value=value, negate=negate))
        elif token:
            parsed.free.append(token.lower())
    return parsed


def execute(db: LazyOwnDB | None, query: str, workspace_name: str = "default", db_path: str | None = None) -> dict:
    """Run a parsed query against the engagement database.

    Args:
        db: Open ``LazyOwnDB``; when None a fresh handle over ``db_path``
            (or the default store) is used and closed afterward.
        query: Raw grammar string (parsed here).
        workspace_name: Workspace to search.
        db_path: Optional database path used when ``db`` is None.

    Returns:
        ``{"hosts": [...], "services": [...], "vulns": [...], "creds": [...],
        "errors": [...]}`` with matched rows only (services carry their
        host's address, vulns and creds are already host-joined).
    """
    parsed = parse(query)
    errors = list(parsed.errors)
    handle = db or LazyOwnDB(db_path)
    workspace_id = handle.default_workspace(workspace_name)
    matched_vulns = [row for row in handle.vuln_list(workspace_id) if _row_match(parsed, row, False)]
    matched_creds = [row for row in handle.cred_list(workspace_id) if _row_match(parsed, row, False)]
    matched_hosts: list[dict] = []
    matched_services: list[dict] = []
    for host in handle.host_list(workspace_id):
        services = handle.service_list(host.get("id"))
        host_match = _row_match(parsed, host, True)
        for service in services:
            service.setdefault("host", host.get("address", ""))
            service.setdefault("hostname", host.get("hostname", ""))
            if not host_match and not _row_match(parsed, service, False):
                continue
            if host_match or _row_match(parsed, service, False):
                matched_services.append(service)
        if host_match:
            matched_hosts.append({key: value for key, value in host.items() if key != "id"})
    if db is None:
        handle.close()
    return {
        "hosts": matched_hosts,
        "services": matched_services,
        "vulns": matched_vulns,
        "creds": matched_creds,
        "errors": errors,
    }


def _row_match(parsed: Query, row: dict, is_host: bool) -> bool:
    """Whether one row satisfies every term and free word.

    Args:
        parsed: Parsed :class:`Query`.
        row: Database row as a plain dict.
        is_host: Host rows merge with their service folds before family
            matching, so spot keys that need a service column never match
            a bare host row.

    Returns:
        True when all must-match terms hit and no exclusion trip. For
        free words False means at least one word is missing.
    """
    for term in parsed.terms:
        hit = _term_hit(term, row, is_host)
        if term.negate and hit:
            return False
        if not term.negate and not hit:
            return False
    haystack = _searchable(row, is_host)
    return all(word in haystack for word in parsed.free)


def _term_hit(term: SearchTerm, row: dict, is_host: bool) -> bool:
    """Evaluate one clamp against a row.

    Args:
        term: Parsed clamp.
        row: Database row as a plain dict.
        is_host: Host-row flag for family-dependent fields.

    Returns:
        True when the field matches the term's value.
    """
    if is_host and term.key in (KEY_PORT, KEY_SERVICE, KEY_PRODUCT, KEY_VERSION, KEY_CVE, KEY_USER):
        return False
    if term.key == KEY_PORT:
        return str(row.get("port") or "").strip() == term.value
    if term.key == KEY_HOST:
        fields = f"{row.get('host') or row.get('address') or ''} {row.get('hostname') or ''}".lower()
        return term.value in fields
    if term.key == KEY_SEVERITY:
        return term.value in SEVERITY_SYNONYMS.get(str(row.get("severity") or row.get("name") or "").strip().lower(), "")
    if term.key == KEY_CVE:
        return term.value in str(row.get("name") or "").lower()
    if term.key == KEY_USER:
        return term.value in str(row.get("username") or "").lower()
    if not is_host and term.key in (KEY_SERVICE, KEY_PRODUCT, KEY_VERSION, KEY_STATE, KEY_OS):
        if term.key in (KEY_SERVICE, KEY_PRODUCT, KEY_VERSION):
            return term.value in (str(row.get(term.key) or "") + " " + str(row.get("name") or "")).lower()
        return term.value in str(row.get(term.key) or "").lower()
    return False


def _searchable(row: dict, is_host: bool) -> str:
    """Build the free-word haystack for a row.

    Args:
        row: Database row as a plain dict.
        is_host: Host-row flag.

    Returns:
        Lowercase joined searchable text.
    """
    if is_host:
        parts = [str(row.get(key) or "") for key in ("address", "hostname", "os", "state", "mac")]
    else:
        parts = [str(row.get(key) or "") for key in ("address", "host", "name", "product", "service", "version", "username", "realm", "notes", "description", "severity")]
    return " ".join(parts).lower()


def _canon(key: str, value: str) -> str:
    """Canonicalize a spot-key value before comparison.

    Args:
        key: Normalized spot-key name.
        value: Raw value token.

    Returns:
        Canonical value, empty for a bare severity alias.
    """
    if key == KEY_SEVERITY:
        return SEVERITY_SYNONYMS.get(value, value)
    return value


__all__ = [
    "KEY_ALIASES",
    "Query",
    "SearchTerm",
    "SEVERITY_SYNONYMS",
    "execute",
    "parse",
]

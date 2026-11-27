"""Worker command sanitizer: hallucination and target-drift guards.

Single home for the loop's command sanitation (extracted from
``modules/lazy_loop``): plausible-flag validation, prose detection,
netcat idle-timeout injection and the full ``repair_worker_command``
normalisation (binary-path stripping, invalid nmap port specs, foreign
host retargeting, lost-target repair). Pure string logic — no state.
"""

from __future__ import annotations

import os
import re
import shlex

from modules.loop.flags_catalog import TOOL_LONG_FLAGS

NMAP_LONG_FLAGS = TOOL_LONG_FLAGS["nmap"]
SQLMAP_LONG_FLAGS = TOOL_LONG_FLAGS["sqlmap"]

_TOOL_LONG_FLAGS: dict[str, frozenset[str]] = TOOL_LONG_FLAGS


def plausible_command(command: str) -> bool:
    """Reject obvious hallucinations such as ``nmap --block`` or ``sqlmap --pwn-now``.

    Long flags are validated only for the binaries in :data:`_TOOL_LONG_FLAGS`,
    the tools the loop uses heavily enough that a model invents flags for them;
    every other binary passes untouched, so the filter can never block a
    legitimate operator command for a tool whose flag surface it does not model.
    New tools opt in by adding their stable long-flag set to that map.

    Args:
        command: The candidate command line.

    Returns:
        True when the command is plausible, False when it carries a long flag
        unknown to a validated tool.
    """
    parts = (command or "").strip().split()
    if not parts:
        return True
    allowed = _TOOL_LONG_FLAGS.get(os.path.basename(parts[0]))
    if allowed is None:
        return True
    for token in parts[1:]:
        if token.startswith("--") and token.split("=", 1)[0] not in allowed:
            return False
    return True


_COMMAND_HEAD_RE = re.compile(r"^[A-Za-z0-9_./-]+$")
_ASSIGNMENT_HEAD_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def looks_like_prose(command: str) -> bool:
    """Return True when a line is natural-language prose, not a shell command.

    A hallucinating model sometimes answers a tool prompt with a sentence
    ("Let's proceed step by step ..."), which then fails the shell with a
    quoting error. A real command's first token is a program name or path,
    an assignment, or a subshell; a sentence opens with a word carrying an
    apostrophe, comma or other prose punctuation, or trails a colon after
    several words. Conservative by design: any clean command head passes.

    Args:
        command: Candidate command line.

    Returns:
        True when the line should never be executed as a command.
    """
    text = (command or "").strip()
    if not text:
        return True
    head = text.split()[0]
    if head.startswith(("'", '"', "(", "$", "`", "{")) or _ASSIGNMENT_HEAD_RE.match(text):
        return False
    if not _COMMAND_HEAD_RE.match(head):
        return True
    return text.endswith(":") and len(text.split()) >= 4


def _is_host_like_target(value: str) -> bool:
    """Return True when a target is a routable host worth scope enforcement.

    Scope enforcement applies to hosts, not to local artefacts. Shape and
    file-exclusion policy are the canonical ones in :mod:`core.host_policy`;
    single-host scope checks reject CIDR blocks.
    """
    from core.host_policy import is_engagement_target

    return is_engagement_target(value, allow_cidr=False)


def _is_file_like_value(value: str) -> bool:
    """Return True when value names a local artefact, not a network asset.

    Tool output mentions file names (``scan_x.nmap.xml``, ``report.pdf``)
    that match the subdomain grammar; anchoring them as subdomain assets
    pollutes the asset graph with phantom network entities.
    """
    from core.host_policy import is_file_like

    return is_file_like(value)


NETWORK_TOOL_HEADS = frozenset(
    {
        "nmap",
        "masscan",
        "curl",
        "wget",
        "dig",
        "host",
        "nslookup",
        "nikto",
        "gobuster",
        "ffuf",
        "feroxbuster",
        "hydra",
        "medusa",
        "ssh",
        "smbclient",
        "smbmap",
        "enum4linux",
        "enum4linux-ng",
        "nxc",
        "netexec",
        "crackmapexec",
        "snmpwalk",
        "snmpcheck",
        "whatweb",
        "nc",
        "ncat",
        "netcat",
    }
)

_NETCAT_HEADS = frozenset({"nc", "ncat", "netcat"})
_NETCAT_HEAD_RE = re.compile(r"\b(?:nc|ncat|netcat)\b")
_NETCAT_TIMED_RE = re.compile(r"(?:^|\s)(?:-w\S*|-q\S*|--timeout=\S*)")


def _netcat_idle_timeout(command: str) -> tuple[str, str]:
    """Bound a netcat command's idle reads without re-quoting the line.

    A bare ``nc host port`` (or a piped one-shot banner sender) idles forever
    on servers that keep the connection open and burns the whole worker
    timeout; ``-w N`` bounds connect and idle reads. The injection is done on
    the raw string so piped quoting (``printf 'payload' | nc ...``) survives.

    Args:
        command: Raw proposed command line.

    Returns:
        ``(command, reason)`` with ``-w 5`` injected after the first netcat
        head when the line carries none; ``reason`` empty when unchanged.
    """
    match = _NETCAT_HEAD_RE.search(command or "")
    if match is None:
        return command, ""
    tail = command[match.start() :]
    if _NETCAT_TIMED_RE.search(" " + tail):
        return command, ""
    repaired = command[: match.start()] + _NETCAT_HEAD_RE.sub(
        lambda m: f"{m.group(0)} -w 5", command[match.start() :], count=1
    )
    return repaired, "injected netcat idle timeout"


NMAP_VALUE_FLAGS = frozenset(
    {
        "-p",
        "-e",
        "-S",
        "-g",
        "-D",
        "-oN",
        "-oX",
        "-oG",
        "-oA",
        "-T",
        "--top-ports",
        "--script",
        "--script-args",
        "--min-rate",
        "--max-rate",
        "--mtu",
        "--ttl",
        "--data-length",
        "--source-port",
        "--max-retries",
        "--host-timeout",
        "--scan-delay",
        "--exclude",
        "--excludefile",
        "--dns-servers",
        "--exclude-ports",
        "--version-intensity",
    }
)

_HOSTNAME_RE = re.compile(r"^(?=.{1,253}$)([A-Za-z0-9_](?:[A-Za-z0-9_-]{0,61}[A-Za-z0-9_])?\.)+[A-Za-z]{2,63}$")

SUDO_UNAVAILABLE_MARKERS = (
    "passwordless sudo unavailable",
    "a terminal is required to read the password",
    "unattended loop has no terminal for the password",
)


def _sudo_unavailable(output: str) -> bool:
    """Return True when a tool aborted because sudo cannot prompt here."""
    text = output or ""
    return any(marker in text for marker in SUDO_UNAVAILABLE_MARKERS)


def _is_ip_literal(value: str) -> bool:
    """Return True when ``value`` parses as an IPv4/IPv6 literal."""
    try:
        import ipaddress

        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


_NMAP_PORT_SPEC_RE = re.compile(r"^[0-9A-Za-z_,:\-]+$")


def _valid_nmap_port_spec(value: str) -> bool:
    """Return True when a value is a plausible nmap ``-p`` specification.

    Service names, ranges, comma lists and the ``-`` full-scan shorthand
    pass. An IP or hostname in the value position is the hallucination
    that produced ``nmap -sV -p 172.17.0.2`` and must be rejected.
    """
    text = str(value or "").strip()
    if not text:
        return False
    if _host_from_token(text):
        return False
    return bool(_NMAP_PORT_SPEC_RE.fullmatch(text))


def repair_worker_command(command: str, target: str) -> tuple[str, str]:
    """Normalize one LLM-proposed worker command.

    Repairs three recurring planner mistakes: absolute paths to shell
    verbs (``/usr/bin/lazynmap``), invalid nmap port arguments that put
    the target in the ``-p`` slot, and commands that lost their target.

    Args:
        command: Raw command proposed by the model.
        target: Authorized intent target.

    Returns:
        Tuple of the repaired command and a short reason (empty when the
        command was already valid).
    """
    if not (command or "").strip() or not target:
        return command, ""
    command, reason = _netcat_idle_timeout(command)
    original = command
    try:
        tokens = shlex.split(command)
    except ValueError:
        return command, ""
    if not tokens:
        return command, ""
    original_head = tokens[0]
    head = os.path.basename(original_head)
    if head != original_head:
        parts = command.split(None, 1)
        command = head + (" " + parts[1] if len(parts) > 1 else "")
        tokens[0] = head
        stripped = f"stripped binary path from {original_head}"
        reason = f"{reason}; {stripped}" if reason else stripped
    if head not in NETWORK_TOOL_HEADS:
        return command, reason
    kept: list[str] = [tokens[0]]
    drop_next = False
    skip_next = False
    for index, token in enumerate(tokens[1:], start=1):
        if drop_next:
            drop_next = False
            continue
        if skip_next:
            kept.append(token)
            skip_next = False
            continue
        if token.startswith("-"):
            if head in ("nmap", "masscan") and token in NMAP_VALUE_FLAGS:
                value = tokens[index + 1] if index + 1 < len(tokens) else ""
                if token in ("-p", "--port") and (not value or not _valid_nmap_port_spec(value)):
                    reason = f"dropped invalid port spec {value!r}"
                    drop_next = bool(value)
                    continue
                kept.append(token)
                skip_next = True
                continue
            if token.startswith("--port="):
                value = token.split("=", 1)[1]
                if value and not _valid_nmap_port_spec(value):
                    reason = f"dropped invalid port spec {value!r}"
                    continue
            kept.append(token)
            continue
        host = _host_from_token(token)
        if host and host != target:
            if _is_ip_literal(host):
                kept.append(token)
                continue
            kept.append(token.replace(host, target))
            reason = f"retargeted {host} to {target}"
            continue
        if host == target:
            kept.append(token)
            continue
        if head in ("nmap", "masscan"):
            continue
        kept.append(token)
    if not any(_host_from_token(token) == target for token in kept[1:]):
        kept.append(target)
    return shlex.join(kept), reason


def _host_from_token(token: str) -> str:
    """Extract the host part of a command token, or empty when none.

    Handles bare IPv4 addresses, bare hostnames, URLs (``http://h:p/x``)
    and ``user@host`` credentials (``ssh admin@srv``) so the worker
    sanitizer can retarget foreign hosts to the intent target.
    """
    value = (token or "").strip().strip("'\"")
    if not value or value.startswith("-"):
        return ""
    if "://" in value:
        try:
            host = value.split("://", 1)[1].split("/", 1)[0]
            host = host.rsplit("@", 1)[-1].split(":", 1)[0]
            return host
        except Exception:
            return ""
    candidate = value.split("/", 1)[0]
    bare = candidate.rsplit("@", 1)[-1]
    bare = bare.split(":", 1)[0] if ":" in bare else bare
    try:
        import ipaddress

        ipaddress.ip_address(bare)
        return bare
    except ValueError:
        pass
    if _HOSTNAME_RE.match(bare):
        return bare
    return ""


__all__ = [
    "NMAP_LONG_FLAGS",
    "SQLMAP_LONG_FLAGS",
    "NETWORK_TOOL_HEADS",
    "NMAP_VALUE_FLAGS",
    "SUDO_UNAVAILABLE_MARKERS",
    "plausible_command",
    "looks_like_prose",
    "repair_worker_command",
]

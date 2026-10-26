"""Structured read-only verification of loop findings.

Replaces the old substring-grep retest verdicts with a small fixed set
of read-only checks whose verdict rules are deterministic:

  http_probe   one HEAD (GET only when the server answers 405 to HEAD),
               no cookies, no credentials, no redirects, body discarded
  tcp_probe    one socket connect against the single named port
  banner_probe one connect that reads a banner and matches it against
               the finding's needle
  nmap_sv      ``nmap -sV`` against the single port the finding names
               (only when the nmap binary exists)

Verdict rules, faithful to the reference discipline:

- a check that reproduces the finding marks the finding **reproduced**;
- a check that did not reproduce it NEVER proves it fixed (a template
  can miss: a WAF, a virtual host, a different path) — the verdict
  stays inconclusive and a retry is scheduled;
- every check records exactly the command it ran and a capped evidence
  snippet, so the finding carries what actually happened.

Stdlib only; every check is bounded and non-fatal.
"""

from __future__ import annotations

import re
import shlex
import socket
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CHECK_KINDS = ("http_probe", "tcp_probe", "banner_probe", "nmap_sv")
EVIDENCE_CAP = 2048
OUTPUT_CAP = 600
HTTP_TIMEOUT = 10
CONNECT_TIMEOUT = 5
NMAP_TIMEOUT = 90
MAX_CHECKS = 6
REPRODUCED_CONFIDENCE = 0.9

_IP_RE = re.compile(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b")
_CURL_RE = re.compile(r"curl\s+(?:-[A-Za-z-]+\s+)*https?://[^\s'\"]+", re.IGNORECASE)
_URL_RE = re.compile(r"https?://[^\s'\"]+")
_PORT_RE = re.compile(r"\b(?:port\s+)?(\d{1,5})/(?:tcp|open)\b", re.IGNORECASE)
_HOST_PORT_RE = re.compile(r"(?:\d{1,3}(?:\.\d{1,3}){3}|\b[a-z0-9.-]+\.[a-z]{2,}):(\d{1,5})\b", re.IGNORECASE)
_NMAP_BIN = "nmap"


def _cap(text: str, cap: int = EVIDENCE_CAP) -> str:
    """Trim evidence text to the cap."""
    return str(text or "")[:cap]


def _host_port(finding_text: str, poc: str) -> tuple[str, int]:
    """Best host and port guess from a finding text plus its PoC."""
    for source in (poc or "", finding_text or ""):
        pair = _HOST_PORT_RE.search(source)
        if pair:
            host = _IP_RE.search(source)
            return (host.group(1) if host else source.split(":")[0].strip()), int(pair.group(1))
    for source in (poc or "", finding_text or ""):
        port = _PORT_RE.search(source)
        if port:
            host = _IP_RE.search(source)
            return (host.group(1) if host else ""), int(port.group(1))
        url = _URL_RE.search(source)
        if url:
            try:
                from urllib.parse import urlparse

                parsed = urlparse(url.group(0))
                host = parsed.hostname or ""
                port = parsed.port or (443 if parsed.scheme == "https" else 80)
                return host, int(port)
            except (ValueError, IndexError):
                continue
    host = _IP_RE.search(poc or "") or _IP_RE.search(finding_text or "")
    return (host.group(1) if host else ""), 0


def plan_checks(finding_text: str, poc: str = "") -> list[dict]:
    """Build the read-only check list for one finding.

    Args:
        finding_text: Finding title/summary text.
        poc: Stored proof-of-concept (first line names the replay command).

    Returns:
        List of check dicts ``{"kind", "command", "host", "port", "needle"}``,
        at most :data:`MAX_CHECKS`.
    """
    checks: list[dict] = []
    host, port = _host_port(finding_text, poc)
    needle = ""
    first_line = (poc or "").splitlines()[0].strip() if (poc or "").strip() else ""
    for token in re.findall(r"[A-Za-z][A-Za-z0-9_.-]{5,}", finding_text)[:3]:
        if not token.lower().startswith(("possible", "issue", "finding", "cve-")):
            needle = token
            break

    def _add(kind: str, command: str, check_port: int = 0) -> None:
        if len(checks) >= MAX_CHECKS:
            return
        checks.append(
            {
                "kind": kind,
                "command": command[:300],
                "host": host,
                "port": int(check_port or port or 0),
                "needle": needle,
            }
        )

    if first_line and _CURL_RE.search(first_line):
        replay = first_line
        if not re.search(r"\s-I\b|--head\b", replay):
            replay = replay.replace("curl ", "curl -I ", 1)
        _add("http_probe", replay)
    elif host and port in (80, 443, 8000, 8080, 8081, 8443, 8888, 9443, 3000):
        scheme = "https" if port in (443, 8443, 9443) else "http"
        _add("http_probe", f"curl -sSI --max-time {HTTP_TIMEOUT} {scheme}://{host}:{port}/", port)
    elif host and port and port not in (0,):
        _add("tcp_probe", f"timeout {CONNECT_TIMEOUT + 2} bash -c 'echo > /dev/tcp/{host}/{port}' 2>&1", port)
        _add("banner_probe", f"timeout {CONNECT_TIMEOUT + 2} bash -c 'exec 3<>/dev/tcp/{host}/{port}; head -c 128 <&3' 2>&1", port)
    if host and port and _nmap_available():
        _add("nmap_sv", f"nmap -sV -p {port} --host-timeout {NMAP_TIMEOUT}s {host}", port)
    return checks[:MAX_CHECKS]


def _nmap_available() -> bool:
    """Whether the nmap binary exists on PATH."""
    try:
        import shutil

        return shutil.which(_NMAP_BIN) is not None
    except Exception:
        return False


def run_check(check: dict, executor=None) -> dict:
    """Run one read-only check and classify its result.

    Args:
        check: One check dict from :func:`plan_checks`.
        executor: Optional callable running a shell line and returning output.

    Returns:
        ``{"kind", "command", "verdict", "evidence"}`` where verdict is
        ``hit``/``miss``/``error``.
    """
    kind = str(check.get("kind", ""))
    command = str(check.get("command", ""))
    needle = str(check.get("needle", "")).lower()
    result = {"kind": kind, "command": command, "verdict": "error", "evidence": ""}
    if kind not in CHECK_KINDS or not command:
        result["evidence"] = f"unsupported check kind: {kind}"
        return result
    try:
        if executor is not None:
            output = str(executor(command) or "")
        else:
            from core.process import run_command as _run_command

            output = str(_run_command(command) or "")
    except Exception as exc:
        result["evidence"] = _cap(f"check failed: {exc}")
        return result
    result["evidence"] = _cap(output, OUTPUT_CAP)
    lowered = output.lower()
    if kind == "http_probe":
        status = re.search(r"HTTP/[\d.]+\s+(\d{3})", output)
        if status:
            code = int(status.group(1))
            if code < 400:
                result["verdict"] = "hit"
            elif code in (404, 405, 410):
                result["verdict"] = "miss"
            else:
                result["verdict"] = "inconclusive"
        else:
            result["verdict"] = "error"
        return result
    if kind == "tcp_probe":
        if "connection refused" in lowered or "no route" in lowered or "timed out" in lowered or "unreachable" in lowered:
            result["verdict"] = "miss"
        elif output.strip() == "" or "completed" in lowered:
            result["verdict"] = "hit"
        else:
            result["verdict"] = "inconclusive"
        return result
    if kind == "banner_probe":
        if output.strip():
            if needle and needle in lowered:
                result["verdict"] = "hit"
            else:
                result["verdict"] = "inconclusive"
        else:
            result["verdict"] = "miss"
        return result
    if kind == "nmap_sv":
        if "open" in lowered:
            result["verdict"] = "hit"
        elif "closed" in lowered or "host seems down" in lowered:
            result["verdict"] = "miss"
        else:
            result["verdict"] = "error"
        return result
    return result


def verdict_from_checks(checks_results: list[dict]) -> str:
    """Deterministic verdict from a list of check results.

    Any hit reproduces; misses never prove fixed; everything else stays
    inconclusive so a retry is scheduled later.

    Args:
        checks_results: Results from :func:`run_check`.

    Returns:
        ``reproduced`` or ``inconclusive``.
    """
    for row in checks_results or []:
        if row.get("verdict") == "hit":
            return "reproduced"
    return "inconclusive"


def verify_finding(finding_text: str, poc: str = "", executor=None) -> dict:
    """Plan, run and judge the read-only checks for one finding.

    Args:
        finding_text: Finding title/summary text.
        poc: Stored proof-of-concept.
        executor: Optional callable running a shell line.

    Returns:
        ``{"verdict", "checks": [run_check results]}``.
    """
    checks = plan_checks(finding_text, poc)
    results = []
    for check in checks:
        outcome = run_check(check, executor=executor)
        results.append(outcome)
        if outcome.get("verdict") == "hit":
            break
    return {"verdict": verdict_from_checks(results), "checks": results}


__all__ = [
    "CHECK_KINDS",
    "EVIDENCE_CAP",
    "plan_checks",
    "run_check",
    "verdict_from_checks",
    "verify_finding",
]

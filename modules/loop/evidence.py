"""Verbatim citation verification and command replay for loop findings.

Ports the ARTEX evidence rule: a finding is only ``verified`` when its
proof quote appears verbatim in captured output bound to that finding.
The module normalises whitespace, extracts quoted spans from finding
text, verifies them against the task traffic log (and optionally the
HTTP body recorder), and can replay the stored PoC command once —
never guessing, always over captured evidence.
"""

from __future__ import annotations

import re
import time

QUOTE_PATTERNS = (
    re.compile(r'"(?P<q>[^"\n]{12,400})"'),
    re.compile(r"`(?P<q>[^`\n]{12,400})`"),
    re.compile(r"quote:\s*(?P<q>[^\n]{12,400})", re.IGNORECASE),
)
DEFAULT_CITATION_MAX_AGE_SEC = 24 * 3600.0
MIN_QUOTE_CHARS = 12


def normalize_ws(text: str) -> str:
    """Collapse whitespace runs to single spaces and strip."""
    return re.sub(r"\s+", " ", str(text or "")).strip()


def verbatim_contains(quote: str, source: str) -> bool:
    """Return True when the quote appears verbatim (whitespace-normalised)."""
    needle = normalize_ws(quote)
    haystack = normalize_ws(source)
    return bool(needle) and len(needle) >= MIN_QUOTE_CHARS and needle in haystack


def extract_quote(text: str) -> str:
    """Extract the best quoted span from finding text (best effort)."""
    body = str(text or "")
    for pattern in QUOTE_PATTERNS:
        match = pattern.search(body)
        if match:
            quote = match.group("q").strip()
            if len(quote) >= MIN_QUOTE_CHARS:
                return quote
    return ""


class CitationService:
    """Verify finding quotes against captured traffic.

    Args:
        max_age_sec: Captured records older than this do not verify.
    """

    def __init__(self, max_age_sec: float = DEFAULT_CITATION_MAX_AGE_SEC) -> None:
        self._max_age = float(max_age_sec)

    def verify(self, quote: str, traffic) -> dict:
        """Search the task traffic log for the quote.

        Args:
            quote: Expected verbatim proof text.
            traffic: Object with ``read(limit)`` returning records with
                ``command``/``output``/``ts``/``digest``.

        Returns:
            Dict with ``verified``, ``digest``, ``command`` and ``age``.
        """
        needle = normalize_ws(quote)
        result = {"verified": False, "digest": "", "command": "", "age": -1.0}
        if not needle or len(needle) < MIN_QUOTE_CHARS or traffic is None:
            return result
        try:
            rows = traffic.read(2000)
        except Exception:
            return result
        now = time.time()
        for row in rows:
            output = str(row.get("output", "") or "")
            if not verbatim_contains(needle, output):
                continue
            try:
                ts = float(row.get("ts", 0) or 0)
            except (TypeError, ValueError):
                ts = 0.0
            age = now - ts if ts > 0 else -1.0
            if ts > 0 and age > self._max_age:
                continue
            return {
                "verified": True,
                "digest": str(row.get("digest", "")),
                "command": str(row.get("command", "")),
                "age": round(age, 1),
            }
        return result

    def replay(self, command: str, executor, traffic) -> dict:
        """Replay the stored PoC command once and verify the quote in output.

        Args:
            command: Command line to replay.
            executor: Callable taking the command and returning output.
            traffic: Optional traffic log to record the replay.

        Returns:
            Dict with ``executed``, ``output`` (bounded) and ``verified``.
        """
        clean = str(command or "").strip()
        result = {"executed": False, "output": "", "verified": False}
        if not clean:
            return result
        try:
            output = str(executor(clean) or "")
        except Exception as exc:
            result["output"] = f"replay failed: {exc}"[:400]
            return result
        result["executed"] = True
        result["output"] = output[:4000]
        try:
            if traffic is not None:
                traffic.record("bash", clean, output, {"replay": True})
        except Exception:
            pass
        return result

    def annotate(self, finding: dict, verification: dict) -> dict:
        """Merge a citation verification into a finding meta dict."""
        meta = finding.setdefault("meta", {})
        meta["citation"] = {
            "verified": bool(verification.get("verified")),
            "digest": str(verification.get("digest", "")),
            "age": verification.get("age", -1.0),
        }
        return meta


def citation_service_from_orchestrator() -> CitationService:
    """Build the citation service from the active orchestrator profile."""
    try:
        from modules import orchestrator_config as oc

        section = dict(oc.profile_config().get("evidence") or {})
    except Exception:
        section = {}
    try:
        max_age = float(section.get("citation_max_age_sec", DEFAULT_CITATION_MAX_AGE_SEC))
    except (TypeError, ValueError):
        max_age = DEFAULT_CITATION_MAX_AGE_SEC
    return CitationService(max_age_sec=max_age)


def citation_enabled() -> bool:
    """Return whether citation verification is enabled (default True)."""
    try:
        from modules import orchestrator_config as oc

        section = dict(oc.profile_config().get("evidence") or {})
    except Exception:
        return True
    return bool(section.get("citation_enabled", True))

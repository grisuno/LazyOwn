"""Observer-style failure attribution for autonomous loop steps.

Every executed step is classified into ``ok``, ``blocked`` or ``error`` so the
planner can change strategy instead of hammering a defence. ``blocked`` means
the target actively refused (a WAF, a 403/429, a rate limiter) rather than the
host tooling failing; that distinction is what lets the loop pivot verbs at a
web application firewall instead of re-issuing the same request until the budget
drains.

The per-verb tally is persisted so a verb the target has repeatedly blocked can
be demoted on the next planner round. Host anti-virus and EDR detections are
deliberately out of scope here: those belong to ``reactive_engine`` which
escalates evasion. This module only attributes target-side refusal and tooling
failure, and never imports the loop runtime so it stays cycle-free.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

OK = "ok"
BLOCKED = "blocked"
ERROR = "error"

_BASE_DIR = Path(__file__).resolve().parent.parent
_DEFAULT_BLOCK_THRESHOLD = 2

_HARD_BLOCKED_MARKERS = (
    "403 forbidden",
    "406 not acceptable",
    "429 too many requests",
    "request blocked",
    "request rejected",
    "access denied",
    "you have been blocked",
    "blocked by",
    "rate limit",
    "rate-limited",
    "too many requests",
)

_VENDOR_MARKERS = (
    "web application firewall",
    "mod_security",
    "modsecurity",
    "cloudflare",
    "akamai",
    "incapsula",
    "imperva",
    "captcha",
)

_REJECT_STATUS = re.compile(r"(?<!\d)(401|403|406|409|429|451|503)(?!\d)")
_REJECT_WORDS = (
    "forbidden",
    "denied",
    "blocked",
    "rejected",
    "not acceptable",
    "unauthorized",
    "challenge",
)

_ERROR_MARKERS = (
    "command not found",
    "connection refused",
    "connection reset",
    "could not resolve",
    "name or service not known",
    "no route to host",
    "network is unreachable",
    "operation timed out",
    "connection timed out",
    "ssl handshake",
)


def _has_reject_signal(text: str) -> bool:
    """Return True when the output carries an explicit rejection signal.

    A CDN or WAF vendor name appears on a successful response just as readily as
    on a block page, so a vendor marker is only a block when a rejecting status
    code or rejection word co-occurs. This is the test that keeps a ``200`` from
    ``server: cloudflare`` from being misread as a block.

    Args:
        text: The lowered command output.

    Returns:
        True when a blocking status code or rejection word is present.
    """
    if _REJECT_STATUS.search(text):
        return True
    return any(word in text for word in _REJECT_WORDS)


def classify(output: str, is_error: bool = False) -> str:
    """Attribute one step's result to ``ok``, ``blocked`` or ``error``.

    A hard rejection marker is a block outright. A bare CDN/WAF vendor name is a
    block only when a rejection signal co-occurs, so a successful recon probe
    that merely observes ``server: cloudflare`` is never demoted. Blocked is
    tested before error so a WAF answer is read as a strategy signal, not a
    transport failure the planner would simply retry.

    Args:
        output: Captured command output.
        is_error: True when the executor already flagged a non-zero result.

    Returns:
        One of :data:`OK`, :data:`BLOCKED`, :data:`ERROR`.
    """
    text = str(output or "").lower()
    if any(marker in text for marker in _HARD_BLOCKED_MARKERS):
        return BLOCKED
    if any(marker in text for marker in _VENDOR_MARKERS) and _has_reject_signal(text):
        return BLOCKED
    if is_error or any(marker in text for marker in _ERROR_MARKERS):
        return ERROR
    return OK


def verb_of(command: str) -> str:
    """Return the leading verb of a command line for per-verb attribution.

    Args:
        command: The executed command line.

    Returns:
        The basename of the first token, or an empty string.
    """
    tokens = str(command or "").strip().split()
    if not tokens:
        return ""
    return os.path.basename(tokens[0])[:64]


class AttributionLedger:
    """Persist per-verb outcome tallies and expose repeatedly-blocked verbs.

    The ledger lives at ``sessions/attribution_<task>.json`` and maps each verb
    to its ``ok``/``blocked``/``error`` counts. It is the single place the
    planner consults to learn which verbs the target keeps refusing.
    """

    def __init__(self, task_id: str = "", base_dir: Path | None = None) -> None:
        """Bind the ledger to a task, creating its file lazily on write.

        Args:
            task_id: Campaign/task identifier; blank uses a shared stream.
            base_dir: Optional directory override for tests.
        """
        root = Path(base_dir) if base_dir is not None else _BASE_DIR / "sessions"
        name = f"attribution_{task_id}.json" if task_id else "attribution.json"
        self._path = root / name

    def _load(self) -> dict:
        """Return the stored tally map, or an empty map when unreadable."""
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def record(self, command: str, classification: str) -> str:
        """Tally one classified step under its verb and persist the ledger.

        The load-mutate-save cycle runs under a cross-process lock so two
        concurrent workers never lose each other's tally, and a persist failure
        returns an empty string rather than the verb, so a caller is never told
        a block was recorded when it was not.

        Args:
            command: The executed command line.
            classification: One of :data:`OK`, :data:`BLOCKED`, :data:`ERROR`.

        Returns:
            The verb the step was tallied under, empty when none was parsed or
            the write failed.
        """
        verb = verb_of(command)
        if not verb or classification not in (OK, BLOCKED, ERROR):
            return ""

        def _apply(data: dict) -> None:
            bucket = data.setdefault(verb, {OK: 0, BLOCKED: 0, ERROR: 0})
            bucket[classification] = int(bucket.get(classification, 0)) + 1

        try:
            from core.atomic_store import update_json

            update_json(self._path, _apply, default={})
        except OSError:
            return ""
        return verb

    def counts(self, verb: str) -> dict:
        """Return the ``ok``/``blocked``/``error`` counts for one verb."""
        bucket = self._load().get(verb_of(verb) if " " in str(verb) else str(verb), {})
        return {OK: int(bucket.get(OK, 0)), BLOCKED: int(bucket.get(BLOCKED, 0)), ERROR: int(bucket.get(ERROR, 0))}

    def blocked_verbs(self, threshold: int = _DEFAULT_BLOCK_THRESHOLD) -> set[str]:
        """Return verbs the target has blocked at least ``threshold`` times.

        A verb that has since produced a success is not demoted: a single later
        ``ok`` clears it, so a transient block does not ban a verb for the rest
        of the campaign.

        Args:
            threshold: Minimum blocked count before a verb is demoted.

        Returns:
            The set of verbs the planner should avoid re-proposing.
        """
        floor = max(1, int(threshold))
        out: set[str] = set()
        for verb, bucket in self._load().items():
            blocked = int(bucket.get(BLOCKED, 0))
            if blocked >= floor and int(bucket.get(OK, 0)) == 0:
                out.add(str(verb))
        return out


__all__ = ["AttributionLedger", "BLOCKED", "ERROR", "OK", "classify", "verb_of"]

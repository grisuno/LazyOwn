"""Bounded chain summarizer for the Lazy autonomous loop.

Ports the durable idea behind context-chain summarization: keep the newest
section verbatim, compress older question/answer pairs into a digest, and
mark compressed regions with an explicit prefix so downstream readers know
they are reading a summary. Budgets are characters (cheap, dependency-free)
instead of tokens.

Stdlib only. An optional ``complete`` callable upgrades truncation digests
into model-written ones; without it the summarizer still bounds context.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

LAZY_DIGEST_PREFIX = "[lazy digest]"
MAX_LAST_SECTION_CHARS = 50 * 1024
MAX_SINGLE_PAIR_CHARS = 16 * 1024
MAX_QA_SECTIONS = 10
MAX_QA_CHARS = 64 * 1024
KEEP_MIN_QA_SECTIONS = 1
RESERVE_FRACTION = 0.25


def _text_of(record: Mapping) -> str:
    """Extract printable text from an activity record."""
    text = str(record.get("text", "") or "")
    worker = str(record.get("worker", "") or "")
    kind = str(record.get("kind", "") or "")
    head = f"[{kind}] {worker}: " if worker or kind else ""
    return f"{head}{text}"


def should_compact(used_chars: int, budget_chars: int) -> bool:
    """Return True when context exceeds the usable budget.

    Args:
        used_chars: Current context size in characters.
        budget_chars: Total context budget in characters.

    Returns:
        True when the usable share (budget minus reserve) is exceeded.
    """
    budget = max(1, int(budget_chars or 0))
    usable = int(budget * (1.0 - RESERVE_FRACTION))
    return int(used_chars or 0) > usable


def summarize_chain(
    records: Sequence[Mapping],
    budget_chars: int = MAX_LAST_SECTION_CHARS * 2,
    complete: Callable[[str], str] | None = None,
) -> list[dict]:
    """Bound a record chain to budget, digesting the oldest pairs.

    The newest section (up to ``MAX_LAST_SECTION_CHARS``) is preserved
    verbatim. Older records collapse into digest records prefixed with
    :data:`LAZY_DIGEST_PREFIX`, keeping at most ``MAX_QA_SECTIONS``
    sections and ``MAX_QA_CHARS`` characters of history.

    Args:
        records: Activity records with worker/kind/text keys.
        budget_chars: Total character budget for the returned chain.
        complete: Optional model callable turning a truncation excerpt
            into a denser digest. Failures fall back to truncation.

    Returns:
        Bounded record list, oldest first, digests marked by prefix.
    """
    items = list(records or [])
    if not items:
        return []
    budget = max(1024, int(budget_chars or 0))
    last: list[Mapping] = []
    last_chars = 0
    for record in reversed(items):
        size = len(_text_of(record))
        if last_chars + size > MAX_LAST_SECTION_CHARS and last:
            break
        last.append(record)
        last_chars += size
    last.reverse()
    older = items[: len(items) - len(last)]
    if not older:
        return [dict(record) for record in last]
    digest_text = _digest(older, complete)
    digest_record = {
        "worker": "lazy_scribe",
        "kind": "digest",
        "text": f"{LAZY_DIGEST_PREFIX} {digest_text}",
    }
    headroom = budget - last_chars - len(digest_record["text"])
    if headroom >= 0:
        return [digest_record] + [dict(record) for record in last]
    trimmed = _truncate_records(last, budget - len(digest_record["text"]) - 256)
    return [digest_record] + trimmed


def _digest(older: Sequence[Mapping], complete: Callable[[str], str] | None) -> str:
    """Compress older records into one dense digest string."""
    pairs: list[str] = []
    pair_chars = 0
    for record in older[-MAX_QA_SECTIONS:]:
        excerpt = _text_of(record)[:MAX_SINGLE_PAIR_CHARS]
        if pair_chars + len(excerpt) > MAX_QA_CHARS and len(pairs) >= KEEP_MIN_QA_SECTIONS:
            break
        pairs.append(excerpt)
        pair_chars += len(excerpt)
    raw = " | ".join(pairs)[:MAX_QA_CHARS]
    if complete is None:
        return raw[:2000]
    try:
        prompt = (
            "Compress these penetration-test observations into one dense "
            "digest. Keep hosts, ports, credentials, versions and outcomes; "
            "drop repetition. Reply with plain text, at most 60 words. "
            f"Observations: {raw[:6000]}"
        )
        answer = complete(prompt) or ""
        return answer.strip()[:2000] or raw[:2000]
    except Exception:
        return raw[:2000]


def _truncate_records(records: Sequence[Mapping], budget: int) -> list[dict]:
    """Keep the newest records fitting into budget characters."""
    kept: list[dict] = []
    used = 0
    for record in reversed(list(records)):
        size = len(_text_of(record))
        if used + size > max(256, int(budget)) and kept:
            break
        kept.append(dict(record))
        used += size
    kept.reverse()
    return kept


__all__ = [
    "KEEP_MIN_QA_SECTIONS",
    "LAZY_DIGEST_PREFIX",
    "MAX_LAST_SECTION_CHARS",
    "MAX_QA_CHARS",
    "MAX_QA_SECTIONS",
    "MAX_SINGLE_PAIR_CHARS",
    "RESERVE_FRACTION",
    "should_compact",
    "summarize_chain",
]

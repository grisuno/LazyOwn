"""LazyPassGen: target-aware weak-password generator for LazyOwn.

Synthesises candidate password lists around one target entity (company or
host name) and seeds them with the local default-credential knowledge base
(``modules.lazy_creds``) plus common suffix/leetspeak mutations, seasons and
recent years. Pure in-memory generation writing one text artefact; no
network, no shell.

>>> from modules import lazypassgen
>>> "acme2025" in lazypassgen.generate("acme")["passwords"]
True
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from modules import lazy_creds

MAX_DEFAULT_SEEDS = 64
MAX_MUTATIONS = 4096

_YEARS = ("2024", "2025", "2026", "2027")
_SEASONS = ("spring", "summer", "autumn", "winter", "verano", "invierno")
_MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)
_SUFFIXES = ("123", "!", "123!", "!!", "1", "@", "$", "qwerty", "pass")
_REPLACEMENTS = (("a", "4"), ("e", "3"), ("i", "1"), ("o", "0"), ("s", "$"))
_DEFAULT_PASSWORDS = ("password", "password1", "p@ssw0rd", "admin", "qwerty", "letmein")


def _split_entities(target: str) -> tuple[str, ...]:
    """Split a target name into base words.

    Args:
        target: Target company/host label (may contain dots, dashes, spaces).

    Returns:
        Distinct lowercase words with at least three characters.
    """
    words = "".join(char if char.isalnum() else " " for char in str(target or "").lower()).split()
    unique: list[str] = []
    for word in words:
        if len(word) >= 3 and word not in unique:
            unique.append(word)
    return tuple(unique)


def _leetspeak(word: str) -> str:
    """Return the leetspeak mutation of one word.

    Args:
        word: Lowercase base word.

    Returns:
        Word with letters substituted for lookalike digits.
    """
    value = word
    for letter, digit in _REPLACEMENTS:
        value = value.replace(letter, digit)
    return value


def _mutations(words: tuple[str, ...]) -> tuple[str, ...]:
    """Compose base, suffixed, leet and time-flavoured candidates.

    Args:
        words: Base words derived from the target.

    Returns:
        Distinct candidates capped at ``MAX_MUTATIONS``.
    """
    candidates: list[str] = []
    for word in words:
        candidates.append(word)
        candidates.append(word.capitalize())
        for suffix in _SUFFIXES:
            candidates.append(f"{word}{suffix}")
            candidates.append(f"{word.capitalize()}{suffix}")
        candidates.append(_leetspeak(word))
        candidates.append(_leetspeak(word.capitalize()))
        for year in _YEARS:
            candidates.append(f"{word}{year}")
            candidates.append(f"{word.capitalize()}{year}")
        for season in _SEASONS:
            candidates.append(f"{word}{season}")
    for baseline in _DEFAULT_PASSWORDS:
        candidates.append(baseline)
        for year in _YEARS:
            candidates.append(f"{baseline}{year}")
        for season in _SEASONS:
            candidates.append(f"{baseline}{season}")
        for month in _MONTHS:
            candidates.append(f"{baseline}{month}")
    deduped: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in deduped:
            deduped.append(candidate)
    return tuple(deduped[:MAX_MUTATIONS])


def generate(target: str) -> dict[str, Any]:
    """Generate the candidate set for one target entity.

    Args:
        target: Target company/host name used for seed mutations.

    Returns:
        Mapping with ``passwords`` (mutation tuple), ``frequent_seeds``
        (default-credential pairs) and ``total``; empty when ``target``
        is empty.
    """
    words = _split_entities(target)
    if not words:
        return {"passwords": (), "frequent_seeds": (), "total": 0}
    mutations = _mutations(words)
    seeds = tuple(lazy_creds.candidates(MAX_DEFAULT_SEEDS))
    total = len(mutations) + len(seeds)
    return {"passwords": mutations, "frequent_seeds": seeds, "total": total}


def export(target: str, path: Path | str) -> dict[str, Any]:
    """Write the generated wordlist as one password per line.

    Args:
        target: Target entity name.
        path: Destination file (created/overwritten).

    Returns:
        Mapping with ``written`` and ``error``.
    """
    result = generate(target)
    if not result["passwords"]:
        return {"written": 0, "error": "empty target"}
    lines = list(result["passwords"])
    try:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except Exception as exc:
        return {"written": 0, "error": str(exc)}
    return {"written": len(lines), "error": ""}


if __name__ == "__main__":
    import sys

    target_arg = " ".join(sys.argv[1:]) or "-"
    generated = generate(target_arg)
    for candidate in generated["passwords"]:
        print(candidate)

"""FactStore hash consumer: crypt hashes -> john/hashcat -> stores.

One bridge from the spool-ingested ``CredentialFact`` rows (crypt family:
``/etc/shadow`` dumps, container-host-mount escapes) into the cracking
pipeline and back into the campaign stores: the LazyOwnDB credentials
table and the loop world model, where unbound ``user:password`` values
become lateral spray candidates for the autonomous planner.
"""

from __future__ import annotations

import logging
from pathlib import Path

from skills.lazyown_facts import Config, FactStore

log = logging.getLogger("crack_consumer")

FACT_CRYPT_HASH_TYPES = frozenset(
    {
        "MD5-crypt",
        "SHA-256-crypt",
        "SHA-512-crypt",
        "bcrypt",
        "yescrypt",
        "gost-yescrypt",
        "scrypt",
        "descrypt",
    }
)

HASHES_FILENAME = "hashes_{host}.txt"


def export_facts(host: str, path: Path, store: FactStore | None = None) -> int:
    """Write one host's crypt-family CredentialFacts as hash lines.

    Args:
        host: Host IP whose spooled facts carry the hashes.
        path: Destination hash file (``user:crypt`` per line).
        store: Optional FactStore override; defaults to production config.

    Returns:
        Number of hash lines written.
    """
    facts = (store or FactStore(Config.default())).facts_for(host)
    if facts is None:
        return 0
    lines = [
        f"{fact.username}:{fact.hash_value}" if fact.username else fact.hash_value
        for fact in facts.credentials
        if fact.hash_value and fact.hash_type in FACT_CRYPT_HASH_TYPES
    ]
    if not lines:
        return 0
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


def consume(
    host: str,
    wordlist: str | None = None,
    cracker: object | None = None,
    store: FactStore | None = None,
    sessions_dir: str | Path | None = None,
) -> dict:
    """Export, crack and import one host's crypt hashes into the stores.

    Fail-open everywhere: a missing FactStore, an empty export or a broken
    backend returns a summary with zero cracked instead of raising, so the
    loop and the CLI keep moving.

    Args:
        host: Host IP whose hashes to consume.
        wordlist: Optional wordlist override for the cracker.
        cracker: Optional pre-built HashCracker (test injection); built
            from config when omitted.
        store: Optional FactStore override.
        sessions_dir: Optional sessions directory for the hash file.

    Returns:
        Summary dict with ``file``, ``identified``, ``cracked``,
        ``db_imported``, ``world_model`` and the cracked ``users``.
    """
    base = Path(sessions_dir) if sessions_dir else Path("sessions")
    hash_file = base / HASHES_FILENAME.format(host=host)
    summary: dict = {
        "file": str(hash_file),
        "identified": 0,
        "cracked": 0,
        "db_imported": 0,
        "world_model": 0,
        "users": [],
    }
    try:
        count = export_facts(host, hash_file, store=store)
    except Exception as exc:
        log.debug("hash export failed for %s: %s", host, exc)
        return summary
    if not count:
        try:
            hash_file.unlink(missing_ok=True)
        except OSError:
            pass
        return summary
    summary["identified"] = count
    if cracker is None:
        from modules.hash_cracker import HashCracker

        cracker = HashCracker(wordlist=wordlist)
    try:
        results = cracker.crack_file(hash_file, wordlist=wordlist)
    except Exception as exc:
        log.debug("crack_file failed for %s: %s", hash_file, exc)
        return summary
    cracked = [result for result in results if getattr(result, "cracked", False)]
    summary["cracked"] = len(cracked)
    summary["users"] = [
        result.hash_value.split(":", 1)[0] if ":" in result.hash_value else ""
        for result in cracked
    ]
    try:
        summary["db_imported"] = int(cracker.import_to_db(cracked, rhost=host) or 0)
    except Exception as exc:
        log.debug("DB import failed for %s: %s", host, exc)
    try:
        summary["world_model"] = int(cracker.import_to_world_model(cracked, host=host) or 0)
    except Exception as exc:
        log.debug("world-model import failed for %s: %s", host, exc)
    return summary


def render_summary(summary: dict) -> list[str]:
    """Render one consume summary as operator lines.

    Args:
        summary: Dict returned by :func:`consume`.

    Returns:
        Human-readable lines, no secret material.
    """
    if not summary.get("identified"):
        return [f"no crypt hashes in the FactStore for {summary.get('file', '')}"]
    lines = [
        f"hashes exported: {summary['identified']} -> {summary['file']}",
        f"cracked: {summary['cracked']}/{summary['identified']}"
        f" db={summary['db_imported']} world_model={summary['world_model']}",
    ]
    users = [user for user in summary.get("users", []) if user]
    if users:
        lines.append("cracked users: " + ", ".join(users[:20]))
    return lines


__all__ = ["FACT_CRYPT_HASH_TYPES", "HASHES_FILENAME", "consume", "export_facts", "render_summary"]

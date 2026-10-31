"""Lazy autofire: exploit intelligence closing the loop into chains.

When an exposure report carries fire-tier matches with bounded evidence,
this contract turns them into a validated read-only confirmation chain:
``assign target`` plus one probe step per match (inline nmap version probe
with a ``verify`` token), capped, deduped and cooled down per
``(target, cve_id)``, finished by a ``lazyintel`` re-evaluation step.

Arming is operator-owned: autofire only writes a chain file when
``payload.json`` says ``"autofire": true``; without it, the chain data is
returned as a proposal and nothing is written. Chain generation rides the
existing contract :func:`modules.chain_synth.write_generated_chain`, so an
invalid chain is never persisted.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from modules import lazy_feedmatch
from modules.chain_synth import write_generated_chain
from modules.lazy_probes import CHECK_VERSION_BANNER, render_check

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
STATE_DIR = SESSIONS_DIR / "autofire"
STATE_FILE = STATE_DIR / "state.json"
CHAINS_DIR = BASE_DIR / "chains"
CHAIN_PREFIX = "lazy_autofire_"

COOLDOWN_SECONDS = 86_400
MAX_FIRE_STEPS = 3
REPORT_TEMPLATE = "sessions/lazy_intel_{target}.json"
TARGET_TOKEN = "<TARGET>"
_CVE_TOKEN = re.compile(r"CVE-\d{4}-\d{4,7}")


def autofire_armed(payload: dict | None) -> bool:
    """Whether the operator armed autofire in ``payload.json``.

    Args:
        payload: The loaded payload configuration.

    Returns:
        True only for an explicit ``"autofire": true``.
    """
    return bool((payload or {}).get("autofire") is True)


def consider_report(
    report: dict,
    chains_dir: Path | str | None = None,
    state_path: Path | str | None = None,
    armed: bool | None = None,
    now: float | None = None,
) -> dict:
    """Turn fire-tier bounded matches into a confirmation chain.

    Args:
        report: Exposure report from :func:`modules.lazy_exposure.generate_report`.
        chains_dir: Optional chains directory override.
        state_path: Optional cooldown state file override.
        armed: Explicit arm override; the default None keeps the write
            side off so only an explicit True may persist a chain file.
        now: Optional clock override for cooldown maths and tests.

    Returns:
        ``{"action": "generated"|"proposed"|"skipped", "path", "errors",
        "reason", "cves", "chain"}``.
    """
    moment = float(now if now is not None else time.time())
    want_write = autofire_armed({}) if armed is None else bool(armed)
    target = str(report.get("target") or "")
    fires = _fire_matches(report)
    if not fires:
        return {"action": "skipped", "reason": "no fire-tier bounded matches", "path": None,
                "errors": [], "cves": [], "chain": None}
    state = _load_state(state_path)
    usable, skipped, covered = _cooldown_filter(fires, state, target, moment, chains_dir=str(chains_dir or CHAINS_DIR))
    if not usable:
        reason = "already covered by an existing chain" if covered else "cooldown active for all fire matches"
        return {"action": "skipped", "reason": reason, "path": None,
                "errors": [], "cves": [row["cve_id"] for row in skipped], "chain": None}
    chain_data = _chain_data(target, usable[: MAX_FIRE_STEPS])
    used_fires = chain_data.pop("_used_fires", usable[: MAX_FIRE_STEPS])
    store_path = Path(chains_dir or CHAINS_DIR)
    if not want_write:
        return {"action": "proposed", "reason": "autofire not armed (assign autofire true to write chains)",
                "path": None, "errors": [], "cves": [row["cve_id"] for row in used_fires],
                "chain": chain_data}
    written, errors = write_generated_chain(chain_data, chains_dir=store_path)
    if errors or written is None:
        return {"action": "proposed", "reason": f"chain validation failed: {'; '.join(errors)}",
                "path": None, "errors": errors, "cves": [row["cve_id"] for row in used_fires],
                "chain": chain_data}
    _stamp_cooldown(state, target, [row["cve_id"] for row in used_fires], moment)
    _save_state(state_path, state)
    return {"action": "generated", "reason": "confirmation chain written", "path": str(written),
            "errors": [], "cves": [row["cve_id"] for row in used_fires], "chain": chain_data}


def fire_from_file(target: str, feed_path: str | Path | None = None, **kwargs) -> dict:
    """Consider the saved exposure report of one target.

    Args:
        target: Host the report was generated for.
        feed_path: Optional exploit feed used to regenerate when the
            saved artefact lacks checks context (unused for reading).
        **kwargs: Forwarded to :func:`consider_report`.

    Returns:
        The :func:`consider_report` result; a skip dict when the report
        artefact is missing or unreadable.
    """
    report_path = SESSIONS_DIR / REPORT_TEMPLATE.format(target=_slug(target))
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"action": "skipped", "reason": f"no saved report at {report_path}", "path": None,
                "errors": [], "cves": [], "chain": None}
    return consider_report(report, **kwargs)


def sweep_state(state_path: Path | str | None = None, now: float | None = None) -> int:
    """Drop expired cooldown entries to keep the state file small.

    Args:
        state_path: Optional state file override.
        now: Optional clock override.

    Returns:
        How many entries were pruned.
    """
    moment = float(now if now is not None else time.time())
    state = _load_state(state_path)
    stale = [key for key, stamp in (state.get("cooldown") or {}).items() if moment - float(stamp) >= COOLDOWN_SECONDS]
    for key in stale:
        (state.get("cooldown") or {}).pop(key, None)
    if stale:
        _save_state(state_path, state)
    return len(stale)


def status(payload: dict | None = None, state_path: Path | str | None = None) -> dict:
    """Summarize autofire for the operator surfaces.

    Args:
        payload: Loaded payload configuration for the armed flag.
        state_path: Optional state file override.

    Returns:
        ``{"armed": bool, "cooldown": int, "entries": {key: stamp}}``.
    """
    state = _load_state(state_path)
    cooldown = state.get("cooldown") or {}
    return {
        "armed": autofire_armed(payload),
        "cooldown": len(cooldown),
        "entries": dict(sorted(cooldown.items(), key=lambda item: item[0])),
    }


def _fire_matches(report: dict) -> list[dict]:
    """Extract fire-tier, in-range matches with a port to probe."""
    fires = []
    for row in report.get("matches") or []:
        if row.get("tier") == "hot" and row.get("evidence") == lazy_feedmatch.EVIDENCE_IN_RANGE:
            try:
                port = int(row.get("port") or 0)
            except (TypeError, ValueError):
                port = 0
            if port:
                fires.append(row)
    return fires


def _cooldown_filter(fires: list[dict], state: dict, target: str, moment: float, chains_dir: str = "") -> tuple[list[dict], list[dict], bool]:
    """Split fire rows into usable ones and the cause of each skip.

    Args:
        fires: Fire-tier rows being considered.
        state: Cooldown state dict (mutated into shape).
        target: Target slug source.
        moment: Current clock value.
        chains_dir: Chain directory searched for already-covered cves.

    Returns:
        ``(usable, skipped, covered_cause)`` where ``covered_cause`` is
        True only when every skip came from an existing chain file.
    """
    slug = _slug(target)
    cooldown = state.setdefault("cooldown", {})
    usable: list[dict] = []
    skipped: list[dict] = []
    cooldown_only: list[bool] = []
    existing = _existing_chain_tokens(chains_dir or CHAINS_DIR, slug)
    for row in fires:
        key = f"{slug}|{row.get('cve_id', '')}"
        stamp = cooldown.get(key)
        fresh = stamp is not None and moment - float(stamp) < COOLDOWN_SECONDS
        covered = row.get("cve_id", "") in existing
        if fresh or covered:
            skipped.append(row)
            cooldown_only.append(bool(stamp) and not covered)
        else:
            usable.append(row)
            cooldown_only.append(False)
    covered_cause = bool(skipped) and not usable and not any(cooldown_only)
    return usable, skipped, covered_cause


def _existing_chain_tokens(chains_dir: str | Path, slug: str) -> set[str]:
    """CVE ids already covered by a chain file for this target."""
    path = Path(chains_dir) / f"{CHAIN_PREFIX}{slug}.yaml"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    return set(_CVE_TOKEN.findall(text))


def _chain_data(target: str, fires: list[dict]) -> dict:
    """Compose the read-only confirmation chain data bundle.

    Args:
        target: Host the chain binds to.
        fires: Fire-tier rows (port, product, ranges, cve_id) pre-filtered.

    Returns:
        A chain dict in the writer's schema.
    """
    slug = _slug(target)
    steps: list[dict] = [
        {
            "id": "scope",
            "phase": "recon",
            "description": "Bind the target this autofire chain was generated for.",
            "run": f"assign target {target}",
        }
    ]
    for index, row in enumerate(fires):
        check = render_check(CHECK_VERSION_BANNER, {
            "port": row["port"],
            "product": row["product"],
            "ranges": (row.get("ranges") or []),
        })
        command = check.command.replace(TARGET_TOKEN, target)
        steps.append({
            "id": f"probe_{index + 1}",
            "phase": "recon",
            "description": f"Read-only confirmation for {row['cve_id']} on {target}.",
            "run": command,
            "verify": str(row.get("product") or ""),
            "continue_on_error": True,
            "timeout": 300,
        })
    steps.append({
        "id": "reevaluate",
        "phase": "report",
        "description": "Re-score the target with fresh evidence.",
        "run": f"lazyintel {target}",
        "continue_on_error": True,
        "sinks": [],
    })
    data = {
        "name": f"{CHAIN_PREFIX}{slug}",
        "description": f"Lazy autofire confirmation chain for {slug}",
        "enabled": True,
        "platforms": ["linux", "windows"],
        "defaults": {},
        "steps": steps,
        "total_timeout": 3600,
    }
    data["_used_fires"] = fires[: MAX_FIRE_STEPS]
    return data


def _load_state(path: str | Path | None) -> dict:
    """Read the cooldown state atomically, defaulting to empty."""
    state_file = Path(path) if path else STATE_FILE
    try:
        data = json.loads(state_file.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"cooldown": {}}
    except (OSError, json.JSONDecodeError):
        return {"cooldown": {}}


def _save_state(path: str | Path | None, state: dict) -> None:
    """Write the cooldown state atomically, best-effort."""
    state_file = Path(path) if path else STATE_FILE
    try:
        state_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = state_file.with_suffix(state_file.suffix + ".tmp")
        tmp.write_text(json.dumps(state, indent=2, default=str), encoding="utf-8")
        import os

        os.replace(tmp, state_file)
    except OSError:
        pass


def _stamp_cooldown(state: dict, target: str, cves: list[str], moment: float) -> None:
    """Record cooldown stamps for the freshly handled cves."""
    cooldown = state.setdefault("cooldown", {})
    for cve in cves:
        cooldown[f"{_slug(target)}|{cve}"] = moment


def _slug(text: str) -> str:
    """Compact a target into a filename fragment safe for chain names."""
    slug = "".join(ch if ch.isalnum() and ch not in "._" else "_" for ch in (text or "").lower())
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug.strip("_") or "target"


__all__ = [
    "CHAIN_PREFIX",
    "CHAINS_DIR",
    "COOLDOWN_SECONDS",
    "MAX_FIRE_STEPS",
    "STATE_FILE",
    "TARGET_TOKEN",
    "autofire_armed",
    "consider_report",
    "fire_from_file",
    "sweep_state",
]

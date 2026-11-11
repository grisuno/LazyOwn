"""CTF signalman: one scoreboard for every recorded capture.

Mined from sapper-v2's signalman (a role the sapper commander invented
to collect unsubmitted flags and score them in one place) and
reimplemented LazyOwn-native. The gym harness records evidence per
vector through ``ctf_capture``; this module sweeps a whole gym catalogue,
re-verifies every not-yet-captured vector against the aggregate evidence
tree once, and renders a single scoreboard: captured, missing and score.

One contract per file (SOLID): catalogue selection, the sweep and the
scoreboard rendering live here. Recording stays in ``ctf_capture`` and
I/O (evidence trees, session dirs) is parameterized, so nothing here
knows about the shell.

Captures never bypass a checker: a vector becomes ``captured`` only when
a checker matches, exactly like a manual ``ctf_capture capture`` run.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from modules import ctf_capture

MAX_EVIDENCE_FILES = 50
MAX_EVIDENCE_BYTES = 200_000

_CATALOGUES: dict[str, Callable[[], Any]] = {}


def _catalogue_modules() -> dict[str, Any]:
    """Import the gym catalogue modules lazily (shell boot cost)."""
    global _CATALOGUES
    if not _CATALOGUES:
        from modules import ad_gym, metasploitable_gym, winbox_gym

        _CATALOGUES = {
            "metasploitable": metasploitable_gym,
            "ad_lab": ad_gym,
            "winbox": winbox_gym,
        }
    return _CATALOGUES


def catalogue_for(scenario: str) -> tuple[list[dict], Callable[[str], Any]]:
    """Resolve one gym scenario into its vectors and lookup callable.

    Args:
        scenario: ``metasploitable``, ``ad_lab`` or ``winbox``.

    Returns:
        The catalogue entry list and the module ``get`` callable.

    Raises:
        ValueError: On an unknown scenario.
    """
    modules = _catalogue_modules()
    module = modules.get(str(scenario or "").strip().lower())
    if module is None:
        raise ValueError(f"unknown gym scenario {scenario!r}; expected one of: {', '.join(sorted(modules))}")
    return module.vulnerabilities(), module.get


def _gather_evidence(search_bases: list[str | Path]) -> str:
    """Concatenate text evidence files for checker verification.

    Args:
        search_bases: Directory trees to scan (files are used directly).

    Returns:
        The concatenated text, bounded by ``MAX_EVIDENCE_FILES`` and
        ``MAX_EVIDENCE_BYTES``.
    """
    parts: list[str] = []
    candidates: list[Path] = []
    for base in search_bases or [Path("sessions")]:
        tree = Path(base)
        if tree.is_file():
            candidates.append(tree)
            continue
        if tree.is_dir():
            candidates.extend(sorted(tree.glob("**/*.txt")))
    for path in candidates[:MAX_EVIDENCE_FILES]:
        try:
            if path.is_file() and path.stat().st_size <= MAX_EVIDENCE_BYTES:
                parts.append(path.read_text(errors="replace"))
        except OSError:
            continue
    return "\n".join(parts)


def collect(
    scenario: str,
    target: str = "",
    sessions_dir: str | Path = "sessions",
    search_bases: list[str | Path] | None = None,
) -> dict:
    """Sweep the whole gym scenario and score every vector in one pass.

    For every catalogue vector without a captured record the aggregate
    evidence tree is verified once through the standard checkers; the
    sweep is idempotent (already captured vectors keep their record).

    Args:
        scenario: Gym scenario name (``metasploitable``, ``ad_lab``).
        target: Attacked host recorded on new captures (defaults to the
            payload ``rhost`` when empty).
        sessions_dir: CTF storage root.
        search_bases: Evidence trees; defaults to the sessions dir.

    Returns:
        Report dict with ``captured``, ``missing``, ``score`` (percent),
        ``total`` and the refreshed ``records``.
    """
    entries, lookup = catalogue_for(scenario)
    resolved_target = str(target or "").strip()
    if not resolved_target:
        try:
            from core.config import load_payload

            resolved_target = str((load_payload() or {}).get("rhost", "") or "")
        except Exception:
            resolved_target = ""
    blob = _gather_evidence(list(search_bases) if search_bases else [sessions_dir])
    captured: list[str] = []
    missing: list[str] = []
    for entry in entries:
        vuln_id = str(entry.get("id") or "")
        if not vuln_id:
            continue
        try:
            record = ctf_capture.capture(vuln_id, resolved_target, output=blob, sessions_dir=sessions_dir, catalogue=lookup)
        except ValueError:
            missing.append(vuln_id)
            continue
        if record.get("status") == "captured":
            captured.append(vuln_id)
        else:
            missing.append(vuln_id)
    total = len(captured) + len(missing)
    return {
        "scenario": str(scenario),
        "target": resolved_target,
        "total": total,
        "captured": sorted(captured),
        "missing": sorted(missing),
        "score": round(100.0 * len(captured) / total, 1) if total else 0.0,
        "records": ctf_capture.list_records(sessions_dir=sessions_dir),
    }


def render_scoreboard(report: dict) -> str:
    """Render the collect report as a compact scoreboard.

    Args:
        report: Report from :func:`collect`.

    Returns:
        Multi-line scoreboard text with severity per captured vector.
    """
    header = (
        f"gym {report.get('scenario', '')} @ {report.get('target', '-')}: "
        f"{len(report.get('captured', []))}/{report.get('total', 0)} captured "
        f"(score {report.get('score', 0.0)}%)"
    )
    lines = [header]
    records = report.get("records") or {}
    for vuln_id in report.get("captured", []):
        record = records.get(vuln_id) or {}
        lines.append(
            f"  [x] {vuln_id}  {str(record.get('name', ''))[:60]}"
            f"  cve={record.get('cve') or '-'}  sev={record.get('severity') or '-'}"
        )
    for vuln_id in report.get("missing", []):
        lines.append(f"  [ ] {vuln_id}")
    return "\n".join(lines)


def save_scoreboard(report: dict, sessions_dir: str | Path = "sessions") -> Path:
    """Persist the scoreboard next to the CTF records.

    Args:
        report: Report from :func:`collect`.
        sessions_dir: CTF storage root.

    Returns:
        The written scoreboard path.
    """
    path = Path(sessions_dir) / "ctf" / "scoreboard.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    tmp.replace(path)
    return path


__all__ = ["catalogue_for", "collect", "render_scoreboard", "save_scoreboard"]

"""Auto-generate the engagement report when a loop or chain run finishes.

This is the single entry point that both the autonomous loop runner
(``modules.lazy_runner``) and the APT chain command invoke on completion,
and that the outcome-bus report sink (``modules.sinks.report``) calls for
terminal chain/report outcomes. It refreshes the legacy session report JSON
rendered by the ``/report`` page and writes a client-ready report (HTML,
Markdown, JSON or PDF) via ``modules.professional_report``.

Everything here is best-effort and never raises: report generation must not
be able to fail an engagement run.
"""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path

log = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_DEFAULT_OUTPUT_DIR = "reports"
_DEFAULT_FORMATS = ("html", "md", "json")
_VALID_FORMATS = ("html", "pdf", "md", "json")
_THROTTLE_SECONDS = 20.0

_lock = threading.Lock()
_last_run_at = 0.0


def normalize_funnel(funnel: object) -> dict:
    """Coerce an attribution funnel into a stage-keyed count map.

    The intel producer (``modules.intel_fusion.write_summary``) emits the
    funnel as an ordered list of ``{"stage", "hosts"}`` rows, while the
    report template consumes it as a dict keyed by stage name. This bridges
    both shapes so the report never fails on a producer-format change.

    Args:
        funnel: Either a list of stage rows, an already-keyed dict, or None.

    Returns:
        A dict mapping each stage label to its integer host count. Empty
        when the input is missing or malformed.
    """
    if isinstance(funnel, dict):
        keyed: dict = {}
        for key, value in funnel.items():
            try:
                keyed[str(key)] = int(value)
            except (TypeError, ValueError):
                keyed[str(key)] = 0
        return keyed
    if isinstance(funnel, list):
        rows: dict = {}
        for row in funnel:
            if not isinstance(row, dict):
                continue
            stage = str(row.get("stage", "")).strip()
            if not stage:
                continue
            try:
                rows[stage] = int(row.get("hosts", 0) or 0)
            except (TypeError, ValueError):
                rows[stage] = 0
        return rows
    return {}


def _load_params() -> dict:
    """Read the current payload, returning an empty dict on any failure.

    Returns:
        The payload mapping, or an empty dict when it cannot be read.
    """
    try:
        from core.config import load_payload

        data = load_payload()
        return data if isinstance(data, dict) else {}
    except Exception as exc:
        log.debug("report autogen: payload unavailable: %s", exc)
        return {}


def _is_enabled(params: dict) -> bool:
    """Resolve the ``auto_report_on_finish`` toggle (default enabled).

    Args:
        params: Payload mapping.

    Returns:
        True when auto-report-on-finish is enabled.
    """
    raw = params.get("auto_report_on_finish", True)
    if isinstance(raw, bool):
        return raw
    return str(raw).strip().lower() in ("1", "true", "yes", "on")


def _resolve_formats(params: dict) -> list[str]:
    """Parse the configured report formats, falling back to the defaults.

    Args:
        params: Payload mapping.

    Returns:
        A de-duplicated list of valid report formats.
    """
    raw = str(params.get("auto_report_formats", "") or "").strip()
    requested = [item.strip().lower() for item in raw.split(",") if item.strip()]
    if not requested:
        requested = list(_DEFAULT_FORMATS)
    seen: list[str] = []
    for fmt in requested:
        if fmt in _VALID_FORMATS and fmt not in seen:
            seen.append(fmt)
    return seen or list(_DEFAULT_FORMATS)


def _resolve_output_dir(params: dict) -> str:
    """Resolve the report output directory (default ``reports/``).

    Args:
        params: Payload mapping.

    Returns:
        The output directory path as a string.
    """
    configured = str(params.get("report_output_path", "") or "").strip()
    return configured or _DEFAULT_OUTPUT_DIR


def generate_campaign_report(
    reason: str = "",
    *,
    force: bool = False,
) -> dict:
    """Refresh the session report and emit client-ready report artifacts.

    Args:
        reason: Short human-readable trigger (e.g. ``"auto_loop done"``);
            recorded in the returned payload for operator visibility.
        force: When True, bypass the throttle that collapses rapid
            successive calls from the same run into a single generation.

    Returns:
        A result dict: ``{"enabled", "reason", "session_refreshed",
        "reports": [paths], "errors": [str]}``. Never raises.
    """
    global _last_run_at
    result: dict = {
        "enabled": False,
        "reason": reason,
        "session_refreshed": False,
        "reports": [],
        "errors": [],
    }
    params = _load_params()

    with _lock:
        now = time.time()
        if not force and (now - _last_run_at) < _THROTTLE_SECONDS:
            result["errors"].append("throttled")
            return result
        _last_run_at = now

    try:
        from modules.c2_surfaces import refresh_session_report

        result["session_refreshed"] = bool(refresh_session_report())
    except Exception as exc:
        result["errors"].append(f"session refresh: {exc}")
        log.debug("report autogen: session refresh failed: %s", exc)

    if not _is_enabled(params):
        return result
    result["enabled"] = True

    output_dir = _resolve_output_dir(params)
    client = str(params.get("domain", "") or params.get("subdomain", "") or "").strip()
    try:
        from modules.professional_report import RedTeamReportGenerator

        generator = RedTeamReportGenerator()
        for fmt in _resolve_formats(params):
            try:
                path = generator.generate(
                    output_dir=output_dir,
                    output_format=fmt,
                    client_name=client or "REDACTED",
                )
                if path:
                    result["reports"].append(str(path))
            except Exception as exc:
                result["errors"].append(f"{fmt}: {exc}")
                log.debug("report autogen: %s report failed: %s", fmt, exc)
    except Exception as exc:
        result["errors"].append(f"generator: {exc}")
        log.debug("report autogen: generator unavailable: %s", exc)

    return result

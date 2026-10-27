"""Beacon dispatch sink: on a foothold, stage the catch-back command.

When the loop or an exploit engine reports a shell on a host, the
operator needs the one-liner that connects that box back to the LazyOwn
C2 listener (``lhost:reverse_shell_port``). This sink stages a
host-tagged dispatch file, mirrors it to the C2 dashboard notes and —
only when ``loop_auto_beacon`` is enabled — copies the command to the
clipboard. Never executes anything on the target.
"""

from __future__ import annotations

from pathlib import Path

from core.hardening import safe_clipboard_copy as _safe_clipboard_copy
from core.hardening import sanitize_filename as _sanitize_filename
from modules.outcome_bus import SESSIONS_DIR, OutcomeEvent
from modules.payload_factory import ReverseShellPayload

_DEFAULT_REV_PORT = 4444


def _load_payload() -> dict:
    """Read the payload configuration (test seam).

    Returns:
        The payload dictionary.
    """
    from core.config import load_payload

    return load_payload() or {}


def _copy_clipboard(text: str) -> bool:
    """Copy text to the clipboard (test seam).

    Args:
        text: Content to copy.

    Returns:
        True when the copy succeeded.
    """
    return _safe_clipboard_copy(text)


def apply(event: OutcomeEvent) -> bool:
    """Stage the catch-back command for one foothold outcome.

    Args:
        event: Outcome to react to.

    Returns:
        True when a dispatch file was written.
    """
    if not event.shell:
        return False
    host = event.host_value
    if not host:
        return False
    payload = _load_payload()
    lhost = str(payload.get("lhost", "") or "")
    if not lhost:
        return False
    try:
        rev_port = int(payload.get("reverse_shell_port") or _DEFAULT_REV_PORT)
    except (TypeError, ValueError):
        rev_port = _DEFAULT_REV_PORT
    command = ReverseShellPayload().generate(lhost=lhost, lport=rev_port, shell_type="bash").decode("utf-8")
    sessions = Path(str(event.metadata.get("sessions_dir") or SESSIONS_DIR))
    target = sessions / f"beacon_dispatch_{_sanitize_filename(host)}.txt"
    try:
        sessions.mkdir(parents=True, exist_ok=True)
        target.write_text(
            f"# Catch-back command for {host} (foothold {event.title or event.source})\n"
            f"# Listener: {lhost}:{rev_port} (C2 /connect terminal)\n"
            f"{command}\n",
            encoding="utf-8",
        )
    except OSError:
        return False
    if payload.get("loop_auto_beacon"):
        try:
            _copy_clipboard(command)
        except Exception:
            pass
    return True


__all__ = ["apply"]

"""Retry sessions - safely relaunch a failed verb or a failed run.

A retry session bundles three things the operator needs after a failure:

- resurrection inputs: the newest failed chain checkpoint or the last
  loop task, so ``retry chain <name>`` / ``retry loop`` restart exactly
  where the previous attempt stopped;
- user-varied configuration: overrides applied on top of the recorded
  variables/flags before the relaunch (``--var key=value`` and the
  ordinary chain/loop flags);
- an optional elevated-operator mode: when the failure was caused by a
  missing sudo/session password, the operator may provide a secret for
  this process only. The secret never appears in argv, log or transcript:
  it lives in a 0600 file under ``sessions/retry/`` and is served through
  ``sudo -A`` (``SUDO_ASKPASS`` helper with 0700 permissions). Both files
  are removed by :func:`clear_sudo_secret`, and an ``atexit`` hook removes
  them even on abnormal interpreter exit.

The elevated mode is opt-in per invocation (``--sudo`` plus an explicit
interactive confirmation), because enabling it means destructive steps
configured by the operator (chains, playbooks, gyms) may now actually
execute with root/elevated privileges. :data:`SUDO_WARNING` is the exact
consent text printed to the operator; callers must resolve it to True
before calling :func:`set_sudo_secret`.
"""

from __future__ import annotations

import atexit
import os
import re
import stat
from collections.abc import Callable
from pathlib import Path

from modules.chain_state import list_checkpoints, load_checkpoint

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSION_DIR = REPO_ROOT / "sessions" / "retry"

SUDO_WARNING = """Pay attention: elevated retry mode.
The provided password enables sudo for this shell session (this process
and captured children). Commands may run with root privileges on the
operator host. Specifically, Destructive Steps configured by you
(destructive chains, playbooks and gym scenarios) can now execute and
have the potential to alter data, disrupt services, or render systems
unusable. Continue only if an authorized testing environment is your
current target.
Type YES (uppercase) to accept, anything else to abort."""

_SESSION_SECRET_MARKER_ENV = "LAZYOWN_RETRY_SUDO"
_ASKPASS_MAX_BYTES = 4096
_SEGMENT_SUDO_RE = re.compile(r"^(?:\s++|[A-Za-z_][A-Za-z_0-9]*+=\S*+\s++)*+(?P<sudo>sudo)(?P<tail>\s|$)")


def is_active() -> bool:
    """Return True when an elevated retry session is currently armed."""
    return os.environ.get(_SESSION_SECRET_MARKER_ENV) == "1"


def secret_enabled_path() -> Path:
    """Return the askpass helper path advertised via ``SUDO_ASKPASS``."""
    path = os.environ.get("SUDO_ASKPASS", "")
    return Path(path) if path else Path()


def _verify_askpass_layout(helper: Path, secret_file: Path) -> bool:
    """Check the on-disk askpass pair exists with correct permissions."""
    if not (helper.is_file() and secret_file.is_file()):
        return False
    try:
        helper_mode = stat.S_IMODE(helper.stat().st_mode)
        secret_mode = stat.S_IMODE(secret_file.stat().st_mode)
    except OSError:
        return False
    return helper_mode & 0o022 == 0 and secret_mode & 0o022 == 0


def sudo_gate_open() -> bool:
    """Return True when armed and the on-disk askpass pair is sound.

    Components reading this (utils.needs_sudo callers, loop guards,
    chain runners) use it instead of a passwordless probe while a retry
    session is active. Soundness is re-checked on disk so a stale or
    tampered environment cannot claim elevation.
    """
    if not is_active():
        return False
    helper = secret_enabled_path()
    secret_file = SESSION_DIR / "sudo.secret"
    return bool(helper) and _verify_askpass_layout(helper, secret_file)


def set_sudo_secret(secret: str) -> Path:
    """Arm the elevated retry session with one secret.

    Args:
        secret: The plain sudo password for this session.

    Returns:
        The askpass helper path set on ``SUDO_ASKPASS``.

    Raises:
        ValueError: When the secret is empty or too long.
        OSError: When the session directory cannot be secured.
    """
    secret = str(secret or "")
    if not secret.strip() or len(secret.encode("utf-8")) > _ASKPASS_MAX_BYTES:
        raise ValueError("sudo secret must be 1-4096 bytes")
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(SESSION_DIR, 0o700)
    secret_file = SESSION_DIR / "sudo.secret"
    helper = SESSION_DIR / "sudo_askpass.sh"
    single_rendered = secret.replace("'", "'\\''")
    secret_file.write_bytes(secret.encode("utf-8"))
    os.chmod(secret_file, 0o600)
    helper.write_text(f"#!/bin/sh\ncat '{SESSION_DIR / 'sudo.secret'}'\n", encoding="utf-8")
    os.chmod(helper, 0o700)
    os.environ["SUDO_ASKPASS"] = str(helper)
    os.environ[_SESSION_SECRET_MARKER_ENV] = "1"
    atexit.register(clear_sudo_secret)
    return helper


def clear_sudo_secret() -> None:
    """Disarm the elevated retry session and wipe the secret from disk."""
    for path in (SESSION_DIR / "sudo.secret", SESSION_DIR / "sudo_askpass.sh"):
        try:
            path.chmod(0o600)
            path.unlink()
        except OSError:
            pass
    os.environ.pop("SUDO_ASKPASS", None)
    os.environ.pop(_SESSION_SECRET_MARKER_ENV, None)


def apply_sudo_askpass(command: str) -> str:
    """Rewrite bare ``sudo`` tokens to ``sudo -A`` for one command.

    Args:
        command: Raw shell command line about to execute.

    Returns:
        The command with the top-level sudo invocations switched to the
        askpass path. Verbs whose internals invoke sudo are unaffected:
        elevated retries for those need passwordless sudo or a changed
        configuration.
    """
    text = str(command or "")
    if not is_active():
        return text
    parts = re.split(r"([;&|])", text)
    rewritten: list[str] = []
    for position, part in enumerate(parts):
        if position % 2:
            rewritten.append(part)
        else:
            rewritten.append(_rewrite_segment(part))
    return "".join(rewritten)


def _rewrite_segment(segment: str) -> str:
    """Splice ``-A`` after the first bare sudo of one shell segment.

    Args:
        segment: A single ``;``/``&``/``|``-separated command part.

    Returns:
        The segment, with the leading ``sudo`` token (after an optional
        whitespace/env-assignment prefix) switched to ``sudo -A``.
    """
    match = _SEGMENT_SUDO_RE.search(segment)
    if match is None:
        return segment
    start = match.start("sudo")
    end = match.end("sudo")
    return f"{segment[:start]}sudo -A{segment[end:]}"


def newest_failed_checkpoint(chain: str = "", run_id: str = "") -> dict | None:
    """Return the freshest unfinished checkpoint of one chain.

    Args:
        chain: Chain name filter; empty accepts any chain.
        run_id: Explicit run id; empty means "newest failed".

    Returns:
        The loaded checkpoint mapping, or None when nothing matches.
    """
    from modules.chain_state import checkpoint_dir

    directory = checkpoint_dir()
    if run_id:
        return load_checkpoint(directory, run_id)
    for row in list_checkpoints(directory=directory, limit=64, chain=chain):
        if row.get("state") != "aborted" and row.get("ok", True):
            continue
        state = load_checkpoint(directory, str(row.get("run_id", "")))
        if state is not None:
            return state
    return None


def resolve_sudo_consent(
    confirmer: Callable[[str], str] | None,
    want_sudo: bool,
) -> tuple[bool, str]:
    """Gate the elevated mode behind an explicit, warned confirmation.

    Args:
        confirmer: Prompt function returning the operator answer; when
            None the flag alone is refused (fail-closed).
        want_sudo: True when ``--sudo`` was requested.

    Returns:
        (armed, note) where armed means set_sudo_secret must be called
        and note is the human reason when refused.
    """
    if not want_sudo:
        return False, ""
    if confirmer is None:
        return False, "--sudo refused: no interactive prompt available"
    answer = (confirmer(SUDO_WARNING) or "").strip()
    if answer.upper() != "YES":
        return False, "--sudo aborted by operator"
    return True, ""


__all__ = [
    "SUDO_WARNING",
    "apply_sudo_askpass",
    "clear_sudo_secret",
    "is_active",
    "newest_failed_checkpoint",
    "resolve_sudo_consent",
    "set_sudo_secret",
    "sudo_gate_open",
]

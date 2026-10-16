"""Non-interactive, agent-safe implementation for atomic_tests / atomic_gen.

Thin CLI wrappers in ``cli/commands/command_and_control_migrated.py``
delegate here. MCP tools and the autonomous loop may call
``run_atomic_tests`` / ``run_atomic_gen`` directly with
``non_interactive=True`` so execution never blocks on ``input()``.

Security invariants:
    1. No shell execution — git sync via safe_run_argv / safe_git_clone.
    2. Technique IDs and GUIDs validated by atomic_resolver.
    3. ``input()`` only when stdin is a TTY and non_interactive is False.
    4. Clipboard failures never abort execution.
    5. Generated filenames derived only from validated IDs.
    6. Credentials read from params or sessions/credentials*.txt without
       echoing secrets to stdout or logs.
"""

from __future__ import annotations

import logging
import os
import re
import shlex
import sys
from pathlib import Path
from typing import Any

log = logging.getLogger("atomic_cli")

_BASE_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"
_TMP_ROOT = Path("/tmp/lazyown_atomic_test")

_FLAG_RE = re.compile(r"--([a-z_]+)(?:=(\S+))?")


def parse_atomic_line(line: str) -> dict[str, Any]:
    """Parse free-form CLI args into a structured request.

    Supported forms (all optional, composable):
        ``T1078`` | ``<guid>`` | ``T1059 --platform linux``
        ``--platform windows --non-interactive --json --limit 3``

    Returns:
        Dict with query, platform, non_interactive, as_json, limit.
    """
    text = (line or "").strip()
    tokens = shlex.split(text) if text else []
    out: dict[str, Any] = {
        "query": "",
        "platform": "",
        "non_interactive": False,
        "as_json": False,
        "limit": 20,
    }
    positionals: list[str] = []
    for token in tokens:
        low = token.lower()
        if low in ("--non-interactive", "--noninteractive", "--batch"):
            out["non_interactive"] = True
        elif low in ("--json",):
            out["as_json"] = True
        elif low.startswith("--platform="):
            out["platform"] = token.split("=", 1)[1]
        elif low == "--platform":
            out["platform"] = "__next__"
        elif low.startswith("--limit="):
            try:
                out["limit"] = max(1, min(int(token.split("=", 1)[1]), 50))
            except ValueError:
                pass
        elif low == "--limit":
            out["limit"] = "__next__"  # type: ignore
        elif out["platform"] == "__next__":
            out["platform"] = token
        elif out["limit"] == "__next__":
            try:
                out["limit"] = max(1, min(int(token), 50))
            except ValueError:
                out["limit"] = 20
        else:
            positionals.append(token)
    if out["platform"] == "__next__":
        out["platform"] = ""
    if out["limit"] == "__next__":
        out["limit"] = 20
    if positionals:
        out["query"] = positionals[0]
        for extra in positionals[1:]:
            if not out["platform"] and extra.lower() in (
                "windows", "macos", "linux", "containers",
            ):
                out["platform"] = extra
    if not sys.stdin.isatty():
        out["non_interactive"] = True
    return out


def _resolver():
    """Import the singleton resolver lazily to keep CLI boot fast."""
    sys.path.insert(0, str(_BASE_DIR / "modules"))
    from atomic_resolver import get_resolver

    return get_resolver()


def _print(shell: Any, text: str) -> None:
    """Print via shell printer when available, else stdout."""
    try:
        from core.console import print_msg

        print_msg(text)
    except Exception:
        print(text)
    _ = shell


def _warn(text: str) -> None:
    try:
        from core.console import print_warn

        print_warn(text)
    except Exception:
        print(f"[!] {text}")


def _wants_interactive(non_interactive: bool) -> bool:
    """Return True only when interactive prompts are allowed."""
    return not non_interactive and sys.stdin.isatty()


def _safe_copy(text: str) -> None:
    """Copy to clipboard without ever raising."""
    try:
        from core.hardening import safe_clipboard_copy

        safe_clipboard_copy(text[:65536])
    except Exception:
        try:
            from utils import copy2clip  # type: ignore

            copy2clip(text[:65536])
        except Exception as exc:
            log.debug("clipboard copy failed: %s", exc)


def _load_credentials(params: dict[str, Any], non_interactive: bool) -> tuple[str, str]:
    """Resolve username/password without leaking secrets to logs."""
    username = str(params.get("username", "") or "")
    password = str(params.get("password", "") or "")
    if username and password:
        return username, password
    try:
        from utils import get_credentials  # type: ignore

        creds = get_credentials()
        if creds:
            return str(creds[0][0]), str(creds[0][1])
    except Exception:
        pass
    if _wants_interactive(non_interactive):
        if not username:
            username = input("    [!] Enter the username: ").strip()
        if not password:
            import getpass

            password = getpass.getpass("    [!] Enter the password: ")
    return username, password


def _prompt_choice(count: int, prompt: str, non_interactive: bool) -> int:
    """Return a 0-based choice; 0 when non-interactive (first match)."""
    if not _wants_interactive(non_interactive):
        return 0
    try:
        raw = input(prompt).strip()
        idx = int(raw) - 1
        if 0 <= idx < count:
            return idx
    except (ValueError, IndexError, EOFError):
        pass
    return -1


def run_atomic_tests(params: dict[str, Any], line: str, shell: Any = None) -> int:
    """Execute the atomic_tests workflow (secure + agent-safe).

    Args:
        params: Live payload params (rhost, domain, rport, ...).
        line: Raw CLI line (query + optional flags).
        shell: Optional parent shell for logcsv.

    Returns:
        0 on success, 1 when no test matched, 2 on usage error.
    """
    from atomic_resolver import build_variables, is_guid, is_mitre_id, render_command

    request = parse_atomic_line(line)
    resolver = _resolver()
    if not resolver.available:
        _warn("Atomic Red Team repo not found. Syncing (git clone, no shell)...")
        resolver.ensure_repo()
    if not resolver.available:
        _warn("Atomic repo unavailable at external/.exploit/atomic-red-team/atomics")
        return 2
    resolver.build_index()

    query = request["query"]
    platform = request["platform"]
    non_interactive = request["non_interactive"]
    limit = int(request["limit"])

    if not query and not platform:
        if _wants_interactive(non_interactive):
            _print(shell, "Select the platform to target:")
            platforms = ["windows", "macos", "linux", "containers"]
            for idx, name in enumerate(platforms, 1):
                _print(shell, f"    {idx}. {name}")
            choice = _prompt_choice(len(platforms), "    [!] Enter the number of the platform: ", non_interactive)
            if choice < 0:
                _warn("Invalid platform selection.")
                return 2
            platform = platforms[choice]
        else:
            _warn("Usage: atomic_tests <TID|guid> [--platform linux] [--non-interactive]")
            return 2

    if platform:
        try:
            from atomic_resolver import normalize_platform

            platform = normalize_platform(platform)
        except ValueError as exc:
            _warn(str(exc))
            return 2

    candidates = []
    if query:
        candidates = resolver.resolve(query, platform=platform)
        if not candidates and (is_mitre_id(query.upper()) or re.match(r"^T\d{1,4}$", query.strip().upper())):
            _warn(f"No tests for {query.upper()} on platform {platform or 'any'}.")
            return 1
        if not candidates and not is_guid(query) and not is_mitre_id(query.upper()):
            _warn(f"Test ID {query} not found (expected T####[.###] or GUID).")
            return 1
    else:
        for mitre_id in sorted(resolver.build_index()):
            candidates.extend(resolver.list_for_technique(mitre_id, platform=platform))
            if len(candidates) >= limit:
                break
        candidates = candidates[:limit]

    if not candidates:
        _warn(f"No tests available for platform: {platform or 'any'}")
        return 1

    if len(candidates) == 1 or non_interactive or not _wants_interactive(non_interactive):
        selected = candidates[0]
        selected_guid = selected.guid
    else:
        _print(shell, f"Available Atomic Red Team tests for {platform or 'any'}:")
        for idx, test in enumerate(candidates[:limit], 1):
            _print(shell, f"{idx}. [{test.mitre_id}] {test.name} Id: {test.guid}")
        choice = _prompt_choice(min(len(candidates), limit), "    [!] Enter the number of the test: ", non_interactive)
        if choice < 0:
            _warn("Invalid choice.")
            return 2
        selected = candidates[choice]
        selected_guid = selected.guid
    if len(candidates) > 1 and (non_interactive or not _wants_interactive(non_interactive)) and query:
        _print(shell, f"Multiple tests for {query.upper()}: using first ({selected.name}).")

    _print(shell, f"Atomic ID: {selected_guid}")
    _print(shell, f"Test: {selected.name}")
    _print(shell, f"MITRE ID: {selected.mitre_id}")
    _print(shell, f"MITRE url: {selected.mitre_url}")
    _print(shell, f"Platforms: {', '.join(selected.platforms)}")

    username, password = _load_credentials(params, non_interactive)
    variables = build_variables(
        selected,
        rhost=str(params.get("rhost", "")),
        domain=str(params.get("domain", "")),
        rport=str(params.get("rport", "")),
        username=username,
        password=password,
    )
    prereq = render_command(selected.prereq_command, variables)
    get_prereq = render_command(selected.get_prereq_command, variables)
    command = render_command(selected.command, variables)
    cleanup = render_command(selected.cleanup_command, variables)

    _print(shell, f"Command: {command[:2000]}")
    for label, snippet in (
        ("Prerequisite", prereq),
        ("Get prerequisite", get_prereq),
        ("Command", command),
        ("Cleanup", cleanup),
    ):
        if snippet:
            _safe_copy(snippet)
            if _wants_interactive(non_interactive):
                try:
                    input(f"    [!] Press Enter after executing the {label.lower()}...")
                except EOFError:
                    break
            else:
                _print(shell, f"[{label}] staged to clipboard (non-interactive, not executed).")
                break
    try:
        if shell is not None and hasattr(shell, "logcsv"):
            shell.logcsv(f"atomic_test {selected.mitre_id} {selected_guid}")
    except Exception as exc:
        log.debug("logcsv failed: %s", exc)
    _print(shell, "Test staging completed.")
    return 0


def _sanitized_script_name(test_id: str, extension: str) -> str:
    """Derive a safe sessions filename from a validated ID."""
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", test_id)[:80].strip("_") or "test"
    return f"atomic_test_{cleaned}{extension}"


def run_atomic_gen(params: dict[str, Any], line: str, shell: Any = None) -> int:
    """Generate test + cleanup scripts for one technique or GUID.

    Args:
        params: Live payload params.
        line: Technique ID or GUID plus optional flags.
        shell: Optional parent shell for logcsv.

    Returns:
        0 on success, 1 when not found, 2 on usage error.
    """
    from atomic_resolver import build_variables, render_command

    request = parse_atomic_line(line)
    query = request["query"]
    if not query:
        _warn("Usage: atomic_gen <TID|guid> [--platform linux] [--non-interactive]")
        return 2
    resolver = _resolver()
    if not resolver.available:
        resolver.ensure_repo()
    if not resolver.available:
        _warn("Atomic repo unavailable at external/.exploit/atomic-red-team/atomics")
        return 2
    candidates = resolver.resolve(query, platform=request["platform"])
    if not candidates:
        _warn(f"No Atomic Red Team tests found for {query}.")
        return 1
    selected = candidates[0]
    if len(candidates) > 1:
        _print(shell, f"Multiple tests for {query}: using first ({selected.name}, {selected.guid}).")

    variables = build_variables(
        selected,
        rhost=str(params.get("rhost", "")),
        domain=str(params.get("domain", "")),
        rport=str(params.get("rport", "")),
    )
    prereq = render_command(selected.prereq_command, variables)
    get_prereq = render_command(selected.get_prereq_command, variables)
    command = render_command(selected.command, variables)
    cleanup = render_command(selected.cleanup_command, variables)

    sessions_path = _SESSIONS_DIR / "temp_uploads"
    sessions_path.mkdir(parents=True, exist_ok=True)
    platform_first = (selected.platforms[0].lower() if selected.platforms else "linux")
    extension = ".ps1" if platform_first == "windows" else ".sh"
    safe_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", selected.guid or selected.mitre_id)[:80]
    test_path = sessions_path / _sanitized_script_name(safe_id, extension)
    clean_path = sessions_path / f"atomic_clean_test_{safe_id}{extension}"

    if platform_first == "windows":
        test_content = (
            f'Start-Transcript -Path "/tmp/lazyown_atomic_test/{safe_id}.log"\n'
            f"{get_prereq}\n{prereq}\n{command}\nStop-Transcript\n"
        )
        clean_content = f"{cleanup}\n"
    else:
        test_content = (
            "#!/bin/sh\n"
            f"# Atomic {selected.mitre_id} {selected.guid}\n"
            f"{get_prereq}\n{prereq}\n{command}\n"
        )
        clean_content = f"#!/bin/sh\n{cleanup}\n"
    test_path.write_text(test_content, encoding="utf-8")
    clean_path.write_text(clean_content, encoding="utf-8")
    try:
        os.chmod(test_path, 0o600)
        os.chmod(clean_path, 0o600)
    except OSError:
        pass

    _print(shell, f"Atomic ID: {selected.guid}")
    _print(shell, f"Test: {selected.name}")
    _print(shell, f"MITRE ID: {selected.mitre_id}")
    _print(shell, f"MITRE url: {selected.mitre_url}")
    _print(shell, f"Test script: {test_path}")
    _print(shell, f"Cleanup script: {clean_path}")
    try:
        if shell is not None and hasattr(shell, "logcsv"):
            shell.logcsv(f"atomic_get {test_path} {clean_path}")
    except Exception as exc:
        log.debug("logcsv failed: %s", exc)
    return 0

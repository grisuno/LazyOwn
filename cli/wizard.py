"""Guided first-run setup wizard for the LazyOwn framework.

Walks the operator through the minimum viable configuration:
  rhost, lhost, domain, device, os_id, api_key, wordlist paths.

Auto-detects sensible defaults (lhost from routing table, device from ip route,
SecLists paths on disk) so experts can just press Enter while novices get clear
explanations of every value.

Design contract:
  - Zero imports from lazyown.py or lazyc2.py (Dependency Inversion).
  - The ``run`` function takes a ``params`` dict and a ``save`` callable; it
    never touches payload.json directly.
  - All output goes through rich so colours work on all terminals.
  - Ctrl-C at any prompt exits the wizard cleanly without saving partial state.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

_console = Console(highlight=False, soft_wrap=True)

_SECLISTS_CANDIDATES = [
    "/usr/share/wordlists/SecLists-master",
    "/usr/share/seclists",
    "/usr/share/wordlists/seclists",
    "/opt/seclists",
]

_WORDLIST_KEYS: dict[str, tuple[str, str]] = {
    "dirwordlist": (
        "Discovery/Web-Content/directory-list-2.3-medium.txt",
        "Directory brute-force wordlist (gobuster, ffuf, feroxbuster)",
    ),
    "usrwordlist": (
        "Usernames/xato-net-10-million-usernames.txt",
        "Username brute-force wordlist (hydra, cme, evil-winrm)",
    ),
    "dnswordlist": (
        "Discovery/DNS/subdomains-top1million-110000.txt",
        "DNS subdomain enumeration wordlist",
    ),
    "iiswordlist": (
        "Discovery/Web-Content/IIS.fuzz.txt",
        "IIS-specific content discovery wordlist",
    ),
}

_IP_RE = re.compile(
    r"^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)


@dataclass
class ReadinessItem:
    """One line in the readiness summary table."""

    label: str
    value: str
    status: str
    hint: str = ""


@dataclass
class WizardResult:
    """Outcome returned by :func:`run`."""

    saved: bool = False
    updates: dict[str, Any] = field(default_factory=dict)
    readiness: list[ReadinessItem] = field(default_factory=list)


def run(
    params: dict[str, Any],
    save: Callable[[str, Any], None],
) -> WizardResult:
    """Run the interactive setup wizard and return a :class:`WizardResult`.

    Args:
        params: Live params dict (in-memory mirror of payload.json).
        save: Callback to persist a single key/value pair.  Signature:
              ``save(key: str, value: Any) -> None``.  Called only for
              values the operator explicitly accepted.

    Returns:
        WizardResult with ``saved=True`` when at least one value was written.
    """
    result = WizardResult()
    _print_header()

    try:
        updates = _collect_values(params)
    except KeyboardInterrupt:
        _console.print("\n[bold yellow]  Wizard cancelled — no changes saved.[/]")
        return result

    if not updates:
        _console.print("[dim]  Nothing changed.[/]")
        result.readiness = _build_readiness(params)
        _print_readiness(result.readiness)
        return result

    for key, value in updates.items():
        try:
            save(key, value)
            params[key] = value
        except Exception as exc:
            _console.print(f"[bold red]  Could not save {key}: {exc}[/]")

    result.saved = bool(updates)
    result.updates = updates
    result.readiness = _build_readiness(params)
    _print_readiness(result.readiness)
    _print_next_steps(params)
    return result


def _print_header() -> None:
    _console.print()
    _console.print(
        Panel(
            "[bold cyan]LazyOwn Setup Wizard[/]\n"
            "[dim]Press [Enter] to keep the current/detected value.  "
            "Press [Ctrl-C] to cancel.[/]",
            border_style="cyan",
            padding=(0, 2),
        )
    )
    _console.print()


def _collect_values(params: dict[str, Any]) -> dict[str, Any]:
    updates: dict[str, Any] = {}

    rhost = _ask_rhost(params.get("rhost"))
    if rhost is not None and rhost != params.get("rhost"):
        updates["rhost"] = rhost

    lhost = _ask_lhost(params.get("lhost"))
    if lhost is not None and lhost != params.get("lhost"):
        updates["lhost"] = lhost

    domain = _ask_domain(params.get("domain"))
    if domain is not None and domain != params.get("domain"):
        updates["domain"] = domain

    device = _ask_device(params.get("device"))
    if device is not None and device != params.get("device"):
        updates["device"] = device

    os_id = _ask_os_id(params.get("os_id", "2"))
    if os_id is not None and str(os_id) != str(params.get("os_id", "2")):
        updates["os_id"] = os_id

    api_key = _ask_api_key(params.get("api_key"))
    if api_key is not None and api_key != params.get("api_key"):
        updates["api_key"] = api_key

    wordlist_updates = _ask_wordlists(params)
    updates.update(wordlist_updates)

    return updates


def _ask_rhost(current: Any) -> str | None:
    _console.print("[bold white]Step 1 of 7 — Target IP (rhost)[/]")
    _console.print(
        "  [dim]The IP address of the machine you are testing.  "
        "Example: 10.10.11.5 or 192.168.1.100[/]"
    )
    prompt = f"  rhost [{current or 'not set'}]: "
    raw = _prompt(prompt)
    if not raw:
        if current:
            _ok(f"Keeping rhost = {current}")
            return None
        _warn("rhost not set — you can set it later with: assign rhost <IP>")
        return None

    if not _IP_RE.match(raw):
        _warn(f"{raw!r} does not look like an IP address — skipping rhost")
        return None

    reachable = _ping(raw)
    if reachable:
        _ok(f"rhost = {raw}  (host responded to ping)")
    else:
        _warn(f"rhost = {raw}  (host did not respond to ping — may still be valid)")
    _console.print()
    return raw


def _ask_lhost(current: Any) -> str | None:
    detected = _detect_lhost()
    effective_default = current or detected
    _console.print("[bold white]Step 2 of 7 — Attacker IP (lhost)[/]")
    _console.print(
        "  [dim]Your machine's IP on the VPN or target network (tun0, eth0, etc.)[/]"
    )
    if detected and detected != current:
        _console.print(f"  [dim cyan]Auto-detected: {detected}[/]")
    prompt = f"  lhost [{effective_default or 'not set'}]: "
    raw = _prompt(prompt)
    if not raw:
        if effective_default and effective_default != current:
            _ok(f"lhost = {effective_default}  (auto-detected)")
            _console.print()
            return effective_default
        if current:
            _ok(f"Keeping lhost = {current}")
        else:
            _warn("lhost not set — set later with: assign lhost <IP>")
        return None

    if not _IP_RE.match(raw):
        _warn(f"{raw!r} does not look like an IP address — skipping lhost")
        return None

    _ok(f"lhost = {raw}")
    _console.print()
    return raw


def _ask_domain(current: Any) -> str | None:
    _console.print("[bold white]Step 3 of 7 — Target domain (optional)[/]")
    _console.print(
        "  [dim]Virtual host or DNS name of the target. Example: target.htb[/]\n"
        "  [dim]Leave blank to skip — needed for vhost-based web apps.[/]"
    )
    prompt = f"  domain [{current or 'skip'}]: "
    raw = _prompt(prompt)
    if not raw:
        if current:
            _ok(f"Keeping domain = {current}")
        else:
            _info("domain not set — can be set later with: assign domain target.htb")
        _console.print()
        return None
    _ok(f"domain = {raw}")
    _console.print()
    return raw


def _ask_device(current: Any) -> str | None:
    detected = _detect_device()
    effective_default = current or detected
    _console.print("[bold white]Step 4 of 7 — Network interface (device)[/]")
    _console.print(
        "  [dim]Interface facing the target network.  "
        "Example: tun0, eth0, ens33[/]"
    )
    if detected and detected != current:
        _console.print(f"  [dim cyan]Auto-detected: {detected}[/]")
    prompt = f"  device [{effective_default or 'not set'}]: "
    raw = _prompt(prompt)
    if not raw:
        if effective_default and effective_default != current:
            _ok(f"device = {effective_default}  (auto-detected)")
            _console.print()
            return effective_default
        if current:
            _ok(f"Keeping device = {current}")
        else:
            _warn("device not set — set later with: assign device eth0")
        return None
    _ok(f"device = {raw}")
    _console.print()
    return raw


def _ask_os_id(current: Any) -> str | None:
    _console.print("[bold white]Step 5 of 7 — Target OS[/]")
    _console.print(
        "  [dim]1 = Linux, 2 = Windows.  "
        "Affects which commands the framework recommends.[/]"
    )
    current_label = "Linux" if str(current) == "1" else "Windows"
    prompt = f"  os_id [{current} = {current_label}]  enter 1 (Linux) or 2 (Windows): "
    raw = _prompt(prompt)
    if not raw:
        _ok(f"Keeping os_id = {current} ({current_label})")
        _console.print()
        return None
    if raw.strip() not in ("1", "2"):
        _warn(f"{raw!r} is not 1 or 2 — keeping {current}")
        _console.print()
        return None
    label = "Linux" if raw.strip() == "1" else "Windows"
    _ok(f"os_id = {raw.strip()} ({label})")
    _console.print()
    return raw.strip()


def _ask_api_key(current: Any) -> str | None:
    _console.print("[bold white]Step 6 of 7 — Groq API key (optional)[/]")
    _console.print(
        "  [dim]Used by AI agents, vuln analysis, and the phishing module.\n"
        "  Get a free key at https://console.groq.com — leave blank to skip.[/]"
    )
    masked = ("*" * 8 + current[-4:]) if (current and len(current) > 8) else (current or "not set")
    prompt = f"  api_key [{masked}]: "
    raw = _prompt(prompt)
    if not raw:
        if current:
            _ok("Keeping existing api_key")
        else:
            _info("api_key not set — AI features will be disabled")
        _console.print()
        return None
    _ok("api_key updated")
    _console.print()
    return raw.strip()


def _ask_wordlists(params: dict[str, Any]) -> dict[str, Any]:
    _console.print("[bold white]Step 7 of 7 — Wordlists (SecLists)[/]")
    base = _find_seclists_root()
    if base:
        _console.print(f"  [dim cyan]SecLists found at: {base}[/]")
    else:
        _warn("SecLists not found.  Install with:")
        _console.print("    [bold]sudo apt install seclists[/]  or")
        _console.print("    [bold]git clone https://github.com/danielmiessler/SecLists /usr/share/wordlists/SecLists-master[/]")
        _console.print()
        return {}

    updates: dict[str, Any] = {}
    for key, (rel_path, description) in _WORDLIST_KEYS.items():
        candidate = Path(base) / rel_path
        current = params.get(key)
        if candidate.exists():
            if str(current) != str(candidate):
                updates[key] = str(candidate)
                _ok(f"{key} = {candidate}")
        else:
            if current and Path(str(current)).exists():
                _info(f"{key}: keeping {current}")
            else:
                _warn(f"{key}: not found at {candidate}")

    _console.print()
    return updates


def _build_readiness(params: dict[str, Any]) -> list[ReadinessItem]:
    items: list[ReadinessItem] = []

    def _check(key: str, label: str, hint: str) -> None:
        val = params.get(key)
        if val:
            items.append(ReadinessItem(label, str(val)[:48], "ok"))
        else:
            items.append(ReadinessItem(label, "not set", "missing", hint))

    _check("rhost", "Target IP (rhost)", "assign rhost <IP>")
    _check("lhost", "Attacker IP (lhost)", "assign lhost <IP>")
    _check("domain", "Domain", "assign domain <name>  (optional)")
    _check("device", "Interface (device)", "assign device eth0")
    _check("api_key", "Groq API key", "assign api_key <key>  (optional)")
    _check("dirwordlist", "Dir wordlist", "install seclists")
    _check("usrwordlist", "User wordlist", "install seclists")

    return items


def _print_readiness(items: list[ReadinessItem]) -> None:
    table = Table(title="Readiness summary", border_style="dim", show_lines=False)
    table.add_column("Setting", style="white", no_wrap=True)
    table.add_column("Value", style="dim white")
    table.add_column("Status", no_wrap=True)
    table.add_column("Hint", style="dim")

    for item in items:
        if item.status == "ok":
            status_cell = Text("ok", style="bold green")
        elif item.status == "missing":
            status_cell = Text("missing", style="bold red")
        else:
            status_cell = Text(item.status, style="yellow")
        table.add_row(item.label, item.value, status_cell, item.hint)

    _console.print()
    _console.print(table)


def _print_next_steps(params: dict[str, Any]) -> None:
    rhost = params.get("rhost")
    _console.print()
    _console.print("[bold cyan]  Suggested next steps:[/]")
    if not rhost:
        _console.print("    1. [bold]assign rhost <target-IP>[/]")
        _console.print("    2. [bold]lazynmap[/]          — full port scan")
    else:
        _console.print(f"    1. [bold]lazynmap[/]          — scan {rhost}")
        _console.print(f"    2. [bold]auto_populate[/]     — populate facts for {rhost}")
        _console.print(f"    3. [bold]palette recon[/]     — browse recon commands")
    _console.print("    Run [bold]wizard[/] again at any time to reconfigure.")
    _console.print()


def _detect_lhost() -> str | None:
    try:
        out = subprocess.check_output(
            ["ip", "route", "get", "8.8.8.8"], text=True, timeout=2, stderr=subprocess.DEVNULL
        )
        m = re.search(r"\bsrc\s+([\d.]+)", out)
        if m and _IP_RE.match(m.group(1)):
            return m.group(1)
    except Exception:
        pass
    try:
        out = subprocess.check_output(
            ["ip", "route", "get", "1.1.1.1"], text=True, timeout=2, stderr=subprocess.DEVNULL
        )
        m = re.search(r"\bsrc\s+([\d.]+)", out)
        if m and _IP_RE.match(m.group(1)):
            return m.group(1)
    except Exception:
        pass
    return None


def _detect_device() -> str | None:
    try:
        out = subprocess.check_output(
            ["ip", "route", "get", "8.8.8.8"], text=True, timeout=2, stderr=subprocess.DEVNULL
        )
        m = re.search(r"\bdev\s+(\S+)", out)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


def _find_seclists_root() -> str | None:
    for candidate in _SECLISTS_CANDIDATES:
        p = Path(candidate)
        if p.is_dir():
            return str(p)
    return None


def _ping(ip: str) -> bool:
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3,
        )
        return result.returncode == 0
    except Exception:
        return False


def _prompt(message: str) -> str:
    try:
        return input(message).strip()
    except EOFError:
        return ""


def _ok(msg: str) -> None:
    _console.print(f"  [bold green]ok[/]  {msg}")


def _warn(msg: str) -> None:
    _console.print(f"  [bold yellow]![/]  {msg}")


def _info(msg: str) -> None:
    _console.print(f"  [dim]--[/]  {msg}")


__all__ = ["WizardResult", "run"]

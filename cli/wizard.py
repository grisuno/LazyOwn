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
import secrets
import shutil
import subprocess
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.payload_schema import (
    Severity,
    coerce_value,
    field_for,
    validate_value,
)

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

_IP_RE = re.compile(r"^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$")

_BINARY_NAME_RE = re.compile(r"\A[A-Za-z0-9_.+-]{1,64}\Z")

_DEFAULT_SECRET_MARKERS = frozenset({"", "change_me"})
_WEAK_SECRET_VALUES = frozenset({"admin", "password", "123456", "lazyown"})
_C2_USER_KEY = "c2_user"
_C2_PASS_KEY = "c2_pass"
_GENERATED_C2_USER = "admin"
_C2_PASS_BYTES = 18


@dataclass(frozen=True)
class BinarySpec:
    """Declarative description of an external tool the framework relies on.

    The wizard verifies presence only — it never executes the binary so a
    malicious shadow ``PATH`` entry cannot be triggered by the readiness
    check itself.

    Attributes:
        name: Executable name as it should appear on ``PATH``. Must
            satisfy :data:`_BINARY_NAME_RE` so logging is safe and the
            value cannot inject shell metacharacters.
        category: Human-readable group used to bucket the report
            (recon, web, smb, ad, exploit, c2).
        purpose: One-line description of why LazyOwn needs the tool.
        install_hint: Operator-facing install command shown when the
            binary is missing. Static string — never interpolated.
    """

    name: str
    category: str
    purpose: str
    install_hint: str


_REQUIRED_BINARIES: tuple[BinarySpec, ...] = (
    BinarySpec("nmap", "recon", "Port and service discovery", "sudo apt install nmap"),
    BinarySpec("curl", "recon", "HTTP probing and beacon delivery", "sudo apt install curl"),
    BinarySpec("ip", "recon", "Routing and interface introspection", "sudo apt install iproute2"),
    BinarySpec("gobuster", "web", "Directory and DNS brute-forcing", "sudo apt install gobuster"),
    BinarySpec("ffuf", "web", "Web fuzzing and parameter discovery", "sudo apt install ffuf"),
    BinarySpec("feroxbuster", "web", "Recursive content discovery", "cargo install feroxbuster"),
    BinarySpec("nikto", "web", "Web server vulnerability scanner", "sudo apt install nikto"),
    BinarySpec("hydra", "cred", "Network login cracker", "sudo apt install hydra"),
    BinarySpec("john", "cred", "Offline password cracker", "sudo apt install john"),
    BinarySpec("hashcat", "cred", "GPU-accelerated cracker", "sudo apt install hashcat"),
    BinarySpec("smbclient", "smb", "SMB share enumeration and access", "sudo apt install smbclient"),
    BinarySpec("enum4linux", "smb", "Linux SMB enumeration", "sudo apt install enum4linux"),
    BinarySpec("crackmapexec", "ad", "AD/SMB authentication sweeps", "pipx install crackmapexec"),
    BinarySpec("impacket-secretsdump", "ad", "Impacket suite — DC dump", "pipx install impacket"),
    BinarySpec("responder", "ad", "LLMNR/NBT-NS poisoning", "sudo apt install responder"),
    BinarySpec("evil-winrm", "ad", "WinRM shell client", "gem install evil-winrm"),
    BinarySpec("searchsploit", "exploit", "Offline Exploit-DB index", "sudo apt install exploitdb"),
    BinarySpec("msfconsole", "exploit", "Metasploit Framework", "sudo apt install metasploit-framework"),
    BinarySpec("tmux", "c2", "Background session multiplexer", "sudo apt install tmux"),
    BinarySpec("openssl", "c2", "Self-signed C2 certificate generation", "sudo apt install openssl"),
    BinarySpec("go", "c2", "Beacon stub compilation", "sudo apt install golang-go"),
)


@dataclass
class BinaryStatus:
    """Result of a presence check for a single :class:`BinarySpec`."""

    spec: BinarySpec
    present: bool
    resolved_path: str | None = None


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
    binaries: list[BinaryStatus] = field(default_factory=list)


def run(
    params: dict[str, Any],
    save: Callable[[str, Any], None],
    *,
    tutorial: bool = False,
) -> WizardResult:
    """Run the interactive setup wizard and return a :class:`WizardResult`.

    Args:
        params: Live params dict (in-memory mirror of payload.json).
        save: Callback to persist a single key/value pair.  Signature:
              ``save(key: str, value: Any) -> None``.  Called only for
              values the operator explicitly accepted.
        tutorial: When ``True`` each step prints the extended help from
            :data:`core.payload_schema.SCHEMA` so first-time operators
            understand *why* each value matters. Veterans omit this and
            just see the auto-detected defaults.

    Returns:
        WizardResult with ``saved=True`` when at least one value was written.
    """
    result = WizardResult()
    _print_header(tutorial=tutorial)
    if tutorial:
        _print_glossary_panel()

    try:
        updates = _collect_values(params, tutorial=tutorial)
    except KeyboardInterrupt:
        _console.print("\n[bold yellow]  Wizard cancelled — no changes saved.[/]")
        return result

    rotated = _rotate_default_secrets(params, save)
    if rotated:
        _print_secret_rotation(rotated)
        result.saved = True

    if not updates:
        _console.print("[dim]  Nothing changed.[/]")
        result.readiness = _build_readiness(params)
        _print_readiness(result.readiness)
        result.binaries = check_binaries()
        _print_binary_report(result.binaries)
        _print_validation_summary(params)
        return result

    for key, value in updates.items():
        try:
            coerced = coerce_value(key, value)
            save(key, coerced)
            params[key] = coerced
        except Exception as exc:
            _console.print(f"[bold red]  Could not save {key}: {exc}[/]")

    result.saved = bool(updates)
    result.updates = updates
    result.readiness = _build_readiness(params)
    _print_readiness(result.readiness)
    result.binaries = check_binaries()
    _print_binary_report(result.binaries)
    _print_validation_summary(params)
    _print_next_steps(params)
    return result


def run_non_interactive(
    params: dict[str, Any],
    save: Callable[[str, Any], None],
    values: dict[str, Any],
    *,
    auto_detect: bool = True,
) -> WizardResult:
    """Apply configuration without prompts — Docker/CI/headless first runs.

    Args:
        params: Live params dict (in-memory mirror of payload.json).
        save: Persistence callback, same contract as :func:`run`.
        values: Keys to apply (``rhost``, ``lhost``, ``domain``, ``device``,
            ``os_id``, ``api_key``). ``None`` values are ignored.
        auto_detect: When ``True`` (default), fill still-empty ``lhost`` /
            ``device`` from the routing table and wordlist paths from
            SecLists, mirroring the interactive wizard's detected defaults.

    Returns:
        WizardResult with ``saved=True`` when at least one value was written.
    """
    result = WizardResult()
    updates: dict[str, Any] = {}
    for key in ("rhost", "lhost", "domain", "device", "os_id", "api_key"):
        value = values.get(key)
        if value is not None and str(value) != str(params.get(key, "")):
            updates[key] = value
    if auto_detect:
        if "lhost" not in updates and not params.get("lhost"):
            detected = _detect_lhost()
            if detected:
                updates["lhost"] = detected
        if "device" not in updates and not params.get("device"):
            detected_dev = _detect_device()
            if detected_dev:
                updates["device"] = detected_dev

    for key, value in updates.items():
        try:
            coerced = coerce_value(key, value)
            save(key, coerced)
            params[key] = coerced
            _ok(f"{key} = {coerced}")
        except Exception as exc:
            _console.print(f"[bold red]  Could not save {key}: {exc}[/]")

    if auto_detect:
        for key, value in _ask_wordlists(params).items():
            try:
                coerced = coerce_value(key, value)
                save(key, coerced)
                params[key] = coerced
            except Exception as exc:
                _console.print(f"[bold red]  Could not save {key}: {exc}[/]")

    rotated = _rotate_default_secrets(params, save)
    if rotated:
        _print_secret_rotation(rotated)

    result.saved = bool(updates) or bool(rotated)
    result.updates = updates
    result.readiness = _build_readiness(params)
    _print_readiness(result.readiness)
    return result


def _rotate_default_secrets(
    params: dict[str, Any],
    save: Callable[[str, Any], None],
) -> list[tuple[str, str]]:
    """Replace factory-default C2 credentials with generated values.

    The example payload ships ``CHANGE_ME`` placeholders; leaving them in
    place means the C2 web console starts with publicly known credentials.
    When the wizard runs, any ``c2_user``/``c2_pass`` still holding a
    default marker is rotated: the user becomes ``admin`` and the password
    a random URL-safe token. Weak but explicitly chosen values (``admin``,
    ``password``...) are warned about, never silently replaced.

    Args:
        params: Live params dict, mutated in place on rotation.
        save: Persistence callback, same contract as :func:`run`.

    Returns:
        List of ``(key, new_value)`` pairs that were rotated.
    """
    rotated: list[tuple[str, str]] = []

    def _is_default(value: Any) -> bool:
        return str(value or "").strip().lower() in _DEFAULT_SECRET_MARKERS

    def _is_weak(value: Any) -> bool:
        return str(value or "").strip().lower() in _WEAK_SECRET_VALUES

    user = params.get(_C2_USER_KEY)
    if _is_default(user):
        save(_C2_USER_KEY, _GENERATED_C2_USER)
        params[_C2_USER_KEY] = _GENERATED_C2_USER
        rotated.append((_C2_USER_KEY, _GENERATED_C2_USER))
    elif _is_weak(user):
        _warn(f"{_C2_USER_KEY} is weak ({user!r}) — consider: assign {_C2_USER_KEY} <name>")

    password = params.get(_C2_PASS_KEY)
    if _is_default(password):
        generated = secrets.token_urlsafe(_C2_PASS_BYTES)
        save(_C2_PASS_KEY, generated)
        params[_C2_PASS_KEY] = generated
        rotated.append((_C2_PASS_KEY, generated))
    elif _is_weak(password):
        _warn(f"{_C2_PASS_KEY} is weak — consider: assign {_C2_PASS_KEY} <strong-password>")

    return rotated


def _print_secret_rotation(rotated: list[tuple[str, str]]) -> None:
    """Tell the operator which credentials were auto-rotated and why."""
    _console.print()
    _console.print(
        Panel(
            "[bold yellow]Default C2 credentials detected and rotated[/]\n"
            + "\n".join(f"  {key} = {value}" for key, value in rotated)
            + "\n[dim]Stored in payload.json — change them anytime with "
            "assign <key> <value>.[/]",
            border_style="yellow",
            padding=(0, 2),
        )
    )
    _console.print()


def _print_header(*, tutorial: bool = False) -> None:
    _console.print()
    subtitle = "[dim]Press [Enter] to keep the current/detected value.  Press [Ctrl-C] to cancel.[/]"
    if tutorial:
        subtitle += "\n[dim cyan]Tutorial mode is on — extended help shown for every step.[/]"
    _console.print(
        Panel(
            "[bold cyan]LazyOwn Setup Wizard[/]\n" + subtitle,
            border_style="cyan",
            padding=(0, 2),
        )
    )
    _console.print()


def _print_glossary_panel() -> None:
    """Print a short glossary so novices understand the recurring terms."""
    body = (
        "[bold]rhost[/] — the target's IP, the box you are attacking.\n"
        "[bold]lhost[/] — your IP on the network or VPN (tun0/eth0).\n"
        "[bold]domain[/] — virtual host name; needed for vhost-based webapps.\n"
        "[bold]device[/] — the interface that reaches the target (tun0, eth0).\n"
        "[bold]os_id[/]  — target OS (1 = Linux, 2 = Windows).\n"
        "[bold]api_key[/] — optional Groq key; unlocks the AI assistants.\n"
        "[bold]wordlists[/] — SecLists paths used by gobuster/ffuf/hydra.\n"
        "Everything is stored in [bold]payload.json[/]. You can change any "
        "value later with [bold]assign <key> <value>[/]."
    )
    _console.print(
        Panel(
            body,
            title="[bold white]What each setting means[/]",
            border_style="dim cyan",
            padding=(0, 2),
        )
    )
    _console.print()


def _spec_long_help(key: str) -> str | None:
    """Return the schema's long_help for ``key`` when it exists."""
    spec = field_for(key)
    if spec is None:
        return None
    return spec.long_help or None


def _print_long_help(key: str) -> None:
    long_help = _spec_long_help(key)
    if long_help:
        for line in long_help.splitlines():
            _console.print(f"  [dim]> {line}[/]")


def _collect_values(params: dict[str, Any], *, tutorial: bool = False) -> dict[str, Any]:
    updates: dict[str, Any] = {}

    rhost = _ask_rhost(params.get("rhost"), tutorial=tutorial)
    if rhost is not None and rhost != params.get("rhost"):
        updates["rhost"] = rhost

    lhost = _ask_lhost(params.get("lhost"), tutorial=tutorial)
    if lhost is not None and lhost != params.get("lhost"):
        updates["lhost"] = lhost

    domain = _ask_domain(params.get("domain"), tutorial=tutorial)
    if domain is not None and domain != params.get("domain"):
        updates["domain"] = domain

    device = _ask_device(params.get("device"), tutorial=tutorial)
    if device is not None and device != params.get("device"):
        updates["device"] = device

    os_id = _ask_os_id(params.get("os_id", "2"), tutorial=tutorial)
    if os_id is not None and str(os_id) != str(params.get("os_id", "2")):
        updates["os_id"] = os_id

    api_key = _ask_api_key(params.get("api_key"), tutorial=tutorial)
    if api_key is not None and api_key != params.get("api_key"):
        updates["api_key"] = api_key

    wordlist_updates = _ask_wordlists(params)
    updates.update(wordlist_updates)

    operator_updates = _ask_operator_login(params, tutorial=tutorial)
    updates.update(operator_updates)

    return updates


def _ask_rhost(current: Any, *, tutorial: bool = False) -> str | None:
    _console.print("[bold white]Step 1 of 7 — Target IP (rhost)[/]")
    _console.print("  [dim]The IP address of the machine you are testing.  Example: 10.10.11.5 or 192.168.1.100[/]")
    if tutorial:
        _print_long_help("rhost")
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


def _ask_lhost(current: Any, *, tutorial: bool = False) -> str | None:
    detected = _detect_lhost()
    effective_default = current or detected
    _console.print("[bold white]Step 2 of 7 — Attacker IP (lhost)[/]")
    _console.print("  [dim]Your machine's IP on the VPN or target network (tun0, eth0, etc.)[/]")
    if tutorial:
        _print_long_help("lhost")
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


def _ask_domain(current: Any, *, tutorial: bool = False) -> str | None:
    _console.print("[bold white]Step 3 of 7 — Target domain (optional)[/]")
    _console.print(
        "  [dim]Virtual host or DNS name of the target. Example: target.htb[/]\n"
        "  [dim]Leave blank to skip — needed for vhost-based web apps.[/]"
    )
    if tutorial:
        _print_long_help("domain")
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


def _ask_device(current: Any, *, tutorial: bool = False) -> str | None:
    detected = _detect_device()
    effective_default = current or detected
    _console.print("[bold white]Step 4 of 7 — Network interface (device)[/]")
    _console.print("  [dim]Interface facing the target network.  Example: tun0, eth0, ens33[/]")
    if tutorial:
        _print_long_help("device")
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


def _ask_os_id(current: Any, *, tutorial: bool = False) -> str | None:
    _console.print("[bold white]Step 5 of 7 — Target OS[/]")
    _console.print("  [dim]1 = Linux, 2 = Windows.  Affects which commands the framework recommends.[/]")
    if tutorial:
        _print_long_help("os_id")
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


def _ask_api_key(current: Any, *, tutorial: bool = False) -> str | None:
    _console.print("[bold white]Step 6 of 7 — Groq API key (optional)[/]")
    _console.print(
        "  [dim]Used by AI agents, vuln analysis, and the phishing module.\n"
        "  Get a free key at https://console.groq.com — leave blank to skip.[/]"
    )
    if tutorial:
        _print_long_help("api_key")
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
        _console.print(
            "    [bold]git clone https://github.com/danielmiessler/SecLists /usr/share/wordlists/SecLists-master[/]"
        )
        _console.print()
        return {}

    updates: dict[str, Any] = {}
    for key, (rel_path, _description) in _WORDLIST_KEYS.items():
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


def _ask_operator_login(params: dict[str, Any], *, tutorial: bool = False) -> dict[str, Any]:
    """Prompt the operator to register or log in, then optionally configure marketplace.

    Args:
        params: Live params dict.
        tutorial: Whether to show extended help.

    Returns:
        Dict with cli_auto_login / cli_remember_token if saved.
    """
    _console.print("[bold white]Step 8 of 8 — Operator identity (required)[/]")
    _console.print(
        "  [dim]The CLI needs to know who you are to track ELO, karma, gym progress,[/]\n"
        "  [dim]and collaboration sessions. Uses the same credentials as the C2 dashboard.[/]"
    )
    _console.print("  [dim]If you skip this, the prompt will show [anonymous] until you 'login'.[/]")
    _console.print()

    from getpass import getpass

    choice = _prompt("  Do you already have an account? (Y/n): ").strip().lower()
    has_account = choice not in ("n", "no")

    if has_account:
        username, password = _wizard_login_flow()
    else:
        username, password = _wizard_register_flow()

    if not username or not password:
        return {}

    try:
        from modules.cli_auth import login

        result = login(username, password, remember=False)
        if not result.get("success"):
            _warn(f"Login failed: {result.get('error', 'unknown')}")
            _info("Use 'login' later to retry.")
            return {}
    except ImportError:
        _warn("Auth module not available — session will be anonymous.")
        return {}

    _ok(f"Authenticated as {username} ({result.get('role')}, {result.get('elo')} ELO)")

    remember = _prompt("  Remember this login? (Y/n): ").strip().lower()
    if remember in ("", "y", "yes"):
        try:
            from modules.cli_auth import login

            login(username, password, remember=True)
            _ok("Remember-me token saved. Auto-login enabled for future sessions.")
            _console.print(
                "  [dim]To disable: assign cli_auto_login \"\" && assign cli_remember_token \"\"[/]"
            )
        except Exception:
            _warn("Could not persist remember-me token.")
    else:
        _info("Login saved for this session only. You'll need to login again next time.")

    _console.print()
    _ask_marketplace_config()

    return {"cli_auto_login": username} if remember in ("", "y", "yes") else {}


def _wizard_login_flow() -> tuple[str | None, str | None]:
    """Handle the login path in the wizard.

    Returns:
        Tuple of (username, password) or (None, None) on skip.
    """
    from getpass import getpass

    username = _prompt("  Username: ").strip()
    if not username:
        _warn("No username provided — session will be anonymous.")
        _info("Use 'login' later to identify yourself and enable ELO tracking.")
        return None, None

    password = getpass("  Password: ")
    if not password:
        _warn("No password provided — session will be anonymous.")
        _info("Use 'login' later to identify yourself and enable ELO tracking.")
        return None, None

    return username, password


def _wizard_register_flow() -> tuple[str | None, str | None]:
    """Handle the register path in the wizard.

    Returns:
        Tuple of (username, password) or (None, None) on skip or failure.
    """
    from getpass import getpass

    username = _prompt("  Choose a username: ").strip()
    if not username:
        _warn("No username provided — session will be anonymous.")
        _info("Use 'register' later to create an account.")
        return None, None

    password = getpass("  Choose a password (min 12 chars): ")
    if not password:
        _warn("No password provided — session will be anonymous.")
        _info("Use 'register' later to create an account.")
        return None, None

    confirm = getpass("  Confirm password: ")
    if password != confirm:
        _warn("Passwords do not match — session will be anonymous.")
        _info("Use 'register' later to retry.")
        return None, None

    try:
        from modules.cli_auth import register
    except ImportError:
        _warn("Auth module not available — session will be anonymous.")
        return None, None

    reg_result = register(username, password)
    if not reg_result.get("success"):
        _warn(f"Registration failed: {reg_result.get('error', 'unknown')}")
        _info("Use 'register' later to retry.")
        return None, None

    _ok(f"Registered as {username} ({reg_result.get('role')})")
    _console.print()
    return username, password


def _ask_marketplace_config() -> None:
    """Optionally launch the interactive marketplace configurator."""
    choice = _prompt("  Review and configure marketplace plugins? (Y/n): ").strip().lower()
    if choice not in ("", "y", "yes"):
        _info("You can configure marketplace plugins later with: marketplace config")
        return

    try:
        from cli.marketplace_config import configure_marketplace_interactive

        _console.print()
        result = configure_marketplace_interactive()
        if result is not None:
            enabled_count = sum(len(v) for v in result.enabled.values())
            _ok(f"Marketplace configured: {enabled_count} addon(s) enabled")
        else:
            _info("Marketplace configuration cancelled.")
    except ImportError:
        _info("Marketplace configurator not available — run 'marketplace config' later.")
    except Exception:
        _info("Marketplace configurator could not start — run 'marketplace config' later.")


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


def check_binaries(
    specs: Sequence[BinarySpec] = _REQUIRED_BINARIES,
    which: Callable[[str], str | None] = shutil.which,
) -> list[BinaryStatus]:
    """Return the presence status of every spec without executing it.

    The check is intentionally side-effect free: it only resolves the
    binary on ``PATH`` via ``shutil.which`` (or the caller-supplied
    equivalent in tests) and never spawns the discovered process. That
    keeps the readiness step deterministic and removes the risk that a
    poisoned ``PATH`` entry could be triggered just by running ``wizard``.

    Args:
        specs: Iterable of :class:`BinarySpec` definitions to verify.
            Defaults to :data:`_REQUIRED_BINARIES`.
        which: ``shutil.which``-compatible callable. Injected so unit
            tests can stub presence detection without touching the
            real ``PATH``.

    Returns:
        A list of :class:`BinaryStatus` items in the same order as
        ``specs``. Binaries whose name fails :data:`_BINARY_NAME_RE`
        are skipped defensively — the module-level constants always
        match, but this guards against future contributions adding
        unsafe entries by mistake.
    """
    statuses: list[BinaryStatus] = []
    for spec in specs:
        if not _BINARY_NAME_RE.match(spec.name):
            continue
        resolved = which(spec.name)
        statuses.append(
            BinaryStatus(
                spec=spec,
                present=bool(resolved),
                resolved_path=resolved if resolved else None,
            )
        )
    return statuses


def _group_by_category(
    statuses: Iterable[BinaryStatus],
) -> dict[str, list[BinaryStatus]]:
    grouped: dict[str, list[BinaryStatus]] = {}
    for status in statuses:
        grouped.setdefault(status.spec.category, []).append(status)
    return grouped


def _print_binary_report(statuses: list[BinaryStatus]) -> None:
    if not statuses:
        return

    missing = [s for s in statuses if not s.present]
    present_count = len(statuses) - len(missing)

    table = Table(
        title=f"External tools  ({present_count}/{len(statuses)} present)",
        border_style="dim",
        show_lines=False,
    )
    table.add_column("Tool", style="white", no_wrap=True)
    table.add_column("Category", style="dim cyan", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("Purpose / install hint", style="dim")

    for category, items in _group_by_category(statuses).items():
        for status in items:
            spec = status.spec
            if status.present:
                cell = Text("ok", style="bold green")
                detail = spec.purpose
            else:
                cell = Text("missing", style="bold red")
                detail = f"{spec.purpose} -- {spec.install_hint}"
            table.add_row(spec.name, category, cell, detail)

    _console.print()
    _console.print(table)

    if missing:
        _console.print(
            f"[bold yellow]  {len(missing)} tool(s) missing — "
            "features that depend on them will be skipped at runtime.[/]"
        )


def _print_next_steps(params: dict[str, Any]) -> None:
    rhost = params.get("rhost")
    _console.print()
    _console.print("[bold cyan]  Suggested next steps:[/]")
    if not rhost:
        _console.print("    1. [bold]assign rhost <target-IP>[/]   set your target")
        _console.print("    2. [bold]lazynmap[/]                  full port + service scan")
        _console.print("    3. [bold]palette recon[/]             browse recon commands")
    else:
        _console.print(f"    1. [bold]ping[/]                     verify {rhost} is up (auto-detects os_id)")
        _console.print(f"    2. [bold]lazynmap[/]                  full port + service scan of {rhost}")
        _console.print("    3. [bold]auto_populate[/]             pull HTB/THM target metadata")
        _console.print("    4. [bold]facts_show[/]                show structured findings")
        _console.print("    5. [bold]recommend_next[/]            phase-aware next command")
    _console.print()
    _console.print(
        "[dim]    Tip: run [bold]wizard --tutorial[/] for extended help, "
        "or [bold]wizard --check[/] for a non-interactive readiness summary.[/]"
    )
    _console.print("[dim]    Edit any value later with [bold]assign <key> <value>[/].[/]")
    _console.print()


def _print_validation_summary(params: dict[str, Any]) -> list[Any]:
    """Render schema validation issues for the current payload.

    Iterates the live params dict, asks the schema for each value, and
    prints a table of problems. The wizard treats errors as blockers and
    warnings as advisory. The returned list lets the caller decide
    whether to short-circuit the post-wizard suggestions.

    Args:
        params: Live params dict after wizard updates have been applied.

    Returns:
        List of :class:`core.payload_schema.ValidationIssue`. Empty when
        every value satisfies the schema.
    """
    issues = []
    for key, value in params.items():
        issue = validate_value(key, value)
        if issue is not None and issue.severity is not Severity.INFO:
            issues.append(issue)

    if not issues:
        return issues

    table = Table(title="Schema warnings", border_style="dim", show_lines=False)
    table.add_column("Field", style="white", no_wrap=True)
    table.add_column("Severity", no_wrap=True)
    table.add_column("Detail", style="dim")
    for issue in issues:
        sev_text = Text(
            issue.severity.value,
            style="bold red" if issue.severity is Severity.ERROR else "yellow",
        )
        table.add_row(issue.key, sev_text, issue.message)
    _console.print()
    _console.print(table)
    return issues


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


__all__ = [
    "BinarySpec",
    "BinaryStatus",
    "WizardResult",
    "check_binaries",
    "run",
    "run_non_interactive",
]

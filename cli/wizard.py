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
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.payload_schema import (
    SCHEMA,
    FieldSpec,
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


def _print_header(*, tutorial: bool = False) -> None:
    _console.print()
    subtitle = (
        "[dim]Press [Enter] to keep the current/detected value.  "
        "Press [Ctrl-C] to cancel.[/]"
    )
    if tutorial:
        subtitle += (
            "\n[dim cyan]Tutorial mode is on — extended help shown for every step.[/]"
        )
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
        _console.print(f"    3. [bold]auto_populate[/]             pull HTB/THM target metadata")
        _console.print(f"    4. [bold]facts_show[/]                show structured findings")
        _console.print("    5. [bold]recommend_next[/]            phase-aware next command")
    _console.print()
    _console.print("[dim]    Tip: run [bold]wizard --tutorial[/] for extended help, "
                   "or [bold]wizard --check[/] for a non-interactive readiness summary.[/]")
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
]

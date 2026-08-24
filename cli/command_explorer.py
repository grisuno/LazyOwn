"""Interactive command explorer by phase and goal for the LazyOwn shell.

Organizes the 727+ commands into user-friendly categories based on what
the operator wants to accomplish, not technical groupings.

Design contract:
    - Zero imports from ``lazyown.py`` or ``lazyc2.py``.
    - All output through ``rich.console.Console``.
    - ``CommandExplorer`` receives its dependencies via constructor.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

_console = Console(highlight=False, soft_wrap=True)

COMMAND_INDEX_PATH = Path("cli/command_index.json")

GOALS: dict[str, dict[str, Any]] = {
    "web": {
        "label": "I found a web service",
        "icon": "HTTP",
        "commands": [
            ("ww", "Fingerprint web technologies"),
            ("gobuster", "Directory brute-force"),
            ("ffuf", "Fast web fuzzer"),
            ("nikto", "Web server vulnerability scanner"),
            ("dirsearch", "Directory and file discovery"),
            ("finalrecon", "All-in-one web recon"),
            ("sqlmap", "SQL injection testing"),
            ("commix", "Command injection testing"),
            ("wfuzz", "Web fuzzing"),
            ("nuclei", "Template-based vulnerability scanning"),
        ],
    },
    "smb_windows": {
        "label": "I found SMB / Windows",
        "icon": "SMB",
        "commands": [
            ("enum4linux", "SMB/LDAP enumeration"),
            ("cme", "Crackmapexec (SMB/AD auth sweeps)"),
            ("getnpusers", "AS-REP roasting"),
            ("secretsdump", "Dump NTDS/SAM/LSA secrets"),
            ("bloodhound", "AD attack path mapping"),
            ("evil", "evil-winrm shell"),
            ("psexec", "Remote execution via SMB"),
            ("ldapdomaindump", "LDAP full dump"),
            ("responder", "LLMNR/NBT-NS poisoning"),
        ],
    },
    "linux_ssh": {
        "label": "I found Linux / SSH",
        "icon": "SSH",
        "commands": [
            ("ssh_cmd", "Run command over SSH"),
            ("scp", "File transfer over SSH"),
            ("linpeas", "Linux privilege escalation checker"),
            ("getcap", "Find Linux capabilities"),
            ("pspy", "Monitor cron and processes"),
        ],
    },
    "shell_payload": {
        "label": "I need a shell / payload",
        "icon": "SHL",
        "commands": [
            ("venom", "Generate msfvenom payload"),
            ("msf", "Start Metasploit handler"),
            ("createrevshell", "Reverse shell one-liner generator"),
            ("blacksandbeacon", "Linux C beacon with BOF support"),
            ("lazymsfvenom", "Generate + deliver beacon"),
            ("createwebshell", "Web shell generator"),
            ("android_apk", "Android APK payload"),
        ],
    },
    "credentials": {
        "label": "I need credentials",
        "icon": "PWD",
        "commands": [
            ("hashcat", "GPU-accelerated password cracking"),
            ("john", "Offline password cracking"),
            ("hydra", "Network login brute-force"),
            ("medusa", "Parallel network brute-force"),
            ("spraykatz", "Credential spraying"),
            ("cewl", "Custom wordlist from website"),
            ("crunch", "Wordlist generator"),
            ("sshkey", "SSH key-based access"),
        ],
    },
    "lateral_movement": {
        "label": "I have creds and want to move",
        "icon": "LAT",
        "commands": [
            ("secretsdump", "Extract hashes and secrets"),
            ("evil", "WinRM shell"),
            ("psexec", "Execute remotely"),
            ("bloodhound", "Map AD attack paths"),
            ("wmiexec", "WMI remote execution"),
            ("chisel", "SOCKS tunnel via SSH"),
        ],
    },
    "privesc": {
        "label": "I want privilege escalation",
        "icon": "PE",
        "commands": [
            ("linpeas", "Linux PE auto-checker"),
            ("winpeas", "Windows PE auto-checker"),
            ("getcap", "Find capabilities for escalation"),
            ("pspy", "Monitor processes for privesc paths"),
        ],
    },
    "persistence": {
        "label": "I want to maintain access",
        "icon": "PST",
        "commands": [
            ("createrevshell", "Persistent reverse shell"),
            ("createwebshell", "Persistent web shell"),
            ("createwinrevshell", "Windows reverse shell"),
            ("backdoor", "Netcat backdoor"),
        ],
    },
    "exfiltration": {
        "label": "I want to exfiltrate data",
        "icon": "EXF",
        "commands": [
            ("scp", "File transfer over SSH"),
            ("smbclient", "SMB file transfer"),
            ("socat", "Bidirectional data transfer"),
            ("dns_exfil", "DNS-based exfiltration"),
        ],
    },
    "recon": {
        "label": "I need situational awareness",
        "icon": "RCN",
        "commands": [
            ("ping", "ICMP alive check + OS detection"),
            ("lazynmap", "Full TCP port scan"),
            ("auto_populate", "Parse scan into context"),
            ("facts_show", "Display discovered facts"),
            ("recommend_next", "AI-ranked next steps"),
            ("sitrep", "Full campaign situation report"),
            ("dashboard", "Full-screen TUI dashboard"),
        ],
    },
    "c2": {
        "label": "I need C2 / implant management",
        "icon": "C2",
        "commands": [
            ("lazyc2", "Start C2 server"),
            ("cc", "Open C2 dashboard"),
            ("collab_join", "Team collaboration URL"),
            ("download_c2", "Download beacon"),
            ("c2_status", "C2 server status"),
            ("c2_beacons", "List connected beacons"),
        ],
    },
    "reporting": {
        "label": "I need to report findings",
        "icon": "RPT",
        "commands": [
            ("campaign_sitrep", "Full situation report"),
            ("report", "Generate report"),
            ("credentials", "List captured credentials"),
            ("timeline", "Red-team timeline"),
            ("session_state", "Session state snapshot"),
        ],
    },
    "autonomous": {
        "label": "I want autonomous / AI operation",
        "icon": "AI",
        "commands": [
            ("auto_pwn", "Autonomous kill-chain walk"),
            ("orchestrate", "Free-text goal to AI backends"),
            ("hunt", "Threat-informed discovery"),
            ("playbook_generate", "Generate attack playbook"),
            ("playbook_run", "Run attack playbook"),
            ("recommend_next", "AI recommends next step"),
        ],
    },
}


@dataclass(frozen=True)
class ExplorerConfig:
    """Centralised constants for the command explorer."""

    index_path: Path = COMMAND_INDEX_PATH


def _load_command_index(path: Path | None = None) -> dict[str, Any]:
    """Load the command index JSON. Returns empty dict on failure."""
    p = path or COMMAND_INDEX_PATH
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


class CommandExplorer:
    """Interactive command explorer organized by user goals.

    Args:
        aliases: Live aliases dict from the shell.
        params: Live params dict from the shell.
        config: Optional config override.
    """

    def __init__(
        self,
        aliases: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        config: ExplorerConfig | None = None,
    ) -> None:
        self._aliases = aliases or {}
        self._params = params or {}
        self._config = config or ExplorerConfig()
        self._index = _load_command_index(self._config.index_path)

    def render_goals_overview(self) -> None:
        """Print the goals table showing all available categories."""
        table = Table(title="Command Explorer -- What do you want to do?", show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=3)
        table.add_column("Goal", style="green")
        table.add_column("Commands", justify="right", style="dim")

        for idx, goal in enumerate(GOALS.values(), 1):
            table.add_row(str(idx), goal["label"], str(len(goal["commands"])))

        _console.print(table)
        _console.print()

    def render_goal_commands(self, goal_key: str) -> None:
        """Print commands for a specific goal."""
        goal = GOALS.get(goal_key)
        if goal is None:
            _console.print(f"[red]Unknown goal '{goal_key}'.[/]")
            return

        table = Table(title=goal["label"], show_header=True, header_style="bold green")
        table.add_column("Command", style="green", min_width=20)
        table.add_column("Description")
        table.add_column("Aliases", style="dim")

        for cmd_name, desc in goal["commands"]:
            aliases = [a for a, t in self._aliases.items() if t == cmd_name]
            alias_str = ", ".join(aliases[:3]) if aliases else ""
            table.add_row(cmd_name, desc, alias_str)

        _console.print(table)
        _console.print()

    def render_search(self, query: str) -> None:
        """Search commands by keyword across all goals."""
        query_lower = query.lower()
        results: list[tuple[str, str, str]] = []

        for _goal_key, goal in GOALS.items():
            for cmd_name, desc in goal["commands"]:
                if query_lower in cmd_name.lower() or query_lower in desc.lower():
                    results.append((cmd_name, desc, goal["label"]))

        if not results:
            _console.print(f"[dim]No commands matching '{query}'.[/]")
            return

        table = Table(title=f"Search results for '{query}'", show_header=True, header_style="bold yellow")
        table.add_column("Command", style="green", min_width=20)
        table.add_column("Description")
        table.add_column("Goal", style="dim")

        for cmd_name, desc, goal_label in results[:20]:
            table.add_row(cmd_name, desc, goal_label)

        if len(results) > 20:
            _console.print(f"[dim]... and {len(results) - 20} more matches[/]")

        _console.print(table)

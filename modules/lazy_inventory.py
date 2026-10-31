"""Host-reported inventory for LazyOwn.

The honest version source: the host itself lists the packages it runs.
This contract renders one read-only collector blob per platform (posix
``sh`` and Windows PowerShell), parses its plain output back into
package/version entries, and promotes them to :class:`Sighting` rows with
``source: "host"`` so the feed matcher can grade services with evidence
no banner could give (a distro backport never changes the banner, the
package table does).

The blob never mutates the host: every command is a read-only query.
"""

from __future__ import annotations

from pathlib import Path

from modules.lazy_feedmatch import Sighting

BASE_DIR = Path(__file__).resolve().parent.parent
SPOOL_DIR = BASE_DIR / "sessions" / "inventory"
SOURCE_HOST = "host"
SOURCE_SCANNER = "scanner"
LINUX_BLOB = "\n".join([
    "set -u",
    "mkdir -p /tmp/lazyinv",
    "{ echo '#LAZYINVENTORY linux'; uname -r; "
    "dpkg-query -W -f='${Package}\\t${Version}\\n' 2>/dev/null "
    "|| rpm -qa --qf '%{NAME}\\t%{VERSION}\\n' 2>/dev/null "
    "|| apk info -v 2>/dev/null; "
    "python3 -m pip list --format=freeze 2>/dev/null | sed 's/==/\\t/g'; } > /tmp/lazyinv/packages.tsv",
    "echo LAZYINVENTORY_DONE",
]) + "\n"
WINDOWS_BLOB = (
    "Set-StrictMode -Version 2\n"
    "Write-Output '#LAZYINVENTORY windows'\n"
    "$paths = @('HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',"
    " 'HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*')\n"
    "Get-ItemProperty $paths -ErrorAction SilentlyContinue |"
    " Where-Object { $_.DisplayName } |"
    " ForEach-Object { \"$($_.DisplayName)`t$($_.DisplayVersion)\" }\n"
    "Write-Output LAZYINVENTORY_DONE\n"
)

BLOBS = {"linux": LINUX_BLOB, "windows": WINDOWS_BLOB}
MAX_ENTRIES = 5000


def inventory_blob(platform: str = "linux") -> str:
    """Return the read-only collector blob for one platform.

    Args:
        platform: ``linux`` (default) or ``windows``.

    Returns:
        The blob text; an empty string for an unknown platform.
    """
    return BLOBS.get(str(platform or "linux").strip().lower(), "")


def parse_blob_output(text: str, platform: str = "linux") -> list[dict]:
    """Parse the collector output into package entries.

    Args:
        text: Raw stdout captured from the blob.
        platform: ``linux`` or ``windows``.

    Returns:
        ``[{"product", "version", "source": "host"}]`` entries, capped at
        :data:`MAX_ENTRIES`. Garbage lines are skipped silently; a done
        marker stops parsing to ignore anything the shell appended.
    """
    marker = "LAZYINVENTORY_DONE"
    entries: list[dict] = []
    kind = "windows" if str(platform or "").strip().lower() == "windows" else "linux"
    body = text.split(marker, 1)[0]
    parse_line = _LINUX_LINE if kind == "linux" else _WINDOWS_LINE
    for line in body.splitlines():
        entry = parse_line(line)
        if entry:
            entries.append(entry)
        if len(entries) >= MAX_ENTRIES:
            break
    return entries


def _LINUX_LINE(line: str) -> dict | None:
    """Parse one ``product<TAB>version`` (or ``prod==ver`` freeze) row."""
    if line.startswith("#"):
        return None
    parts = line.split("\t")
    if len(parts) >= 2:
        product = parts[0].strip()
        version = parts[1].strip()
    else:
        product, version, tail = line.partition("==")
        product = product.strip()
        version = tail.strip()
        if not tail:
            return None
    return _clean_entry(product, version, "linux")


def _WINDOWS_LINE(line: str) -> dict | None:
    """Parse one registry ``DisplayName<TAB>DisplayVersion`` row."""
    if line.startswith("#"):
        return None
    product, _, version = line.partition("\t")
    if not product.strip():
        return None
    return _clean_entry(product.strip().lower(), version.strip().split("\t")[0].strip('"'), "windows")


def _clean_entry(product: str, version: str, os_hint: str) -> dict | None:
    """Validate one parsed package row.

    Args:
        product: Package name text.
        version: Version text.
        os_hint: Platform tag for the entry.

    Returns:
        ``{"product", "version", "source", "os"}`` or None when the row
        lacks a name or any of them is unreasonable.
    """
    if not product or not version or "=" in version or version.endswith(":"):
        return None
    if len(product) < 2 or len(version) > 64:
        return None
    return {"product": product, "version": version, "source": SOURCE_HOST, "os": os_hint}


def to_sightings(entries: list[dict], host: str = "") -> list[Sighting]:
    """Project package entries into host-source sightings.

    Args:
        entries: Parsed package rows from :func:`parse_blob_output`.
        host: Address reporting the inventory.

    Returns:
        One :class:`Sighting` per entry with ``source`` set to
        ``"host"``, port zero (packages are not endpoints).
    """
    return [
        Sighting(
            host=str(host or item.get("host") or ""),
            port=0,
            protocol="pkg",
            product=str(item.get("product") or ""),
            version=str(item.get("version") or ""),
            source=SOURCE_HOST,
        )
        for item in entries
    ]


def os_platform_of(entries: list[dict]) -> str:
    """Detect the inventory platform from the entries' own os tag.

    Args:
        entries: Parsed package rows.

    Returns:
        ``linux`` or ``windows`` (default ``linux``).
    """
    for entry in entries:
        tag = str((entry or {}).get("os") or "").lower()
        if tag in BLOBS:
            return tag
    return "linux"


__all__ = [
    "LINUX_BLOB",
    "MAX_ENTRIES",
    "SOURCE_HOST",
    "SPOOL_DIR",
    "WINDOWS_BLOB",
    "inventory_blob",
    "os_platform_of",
    "parse_blob_output",
    "to_sightings",
]

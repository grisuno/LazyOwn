"""Fail-closed import of attacker-supplied campaign packages.

Campaign ``.zip`` files arrive from other operators and may be
malicious. This module owns the two trust boundaries of the import
path: archive extraction (ZipSlip) and schema merge (second-order
SQL from hostile column names). Callers in ``cli/commands/campaign``
must route through these helpers instead of ``extractall`` and raw
``", ".join(columns)``.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def is_safe_identifier(name: str) -> bool:
    """Return True when ``name`` is a bare SQL identifier.

    Args:
        name: Candidate column or table fragment.

    Returns:
        True for ``[A-Za-z_][A-Za-z0-9_]*``, False otherwise.
    """
    return isinstance(name, str) and _IDENTIFIER_RE.match(name) is not None


def filter_columns(src_columns: list[str], dest_columns: list[str]) -> list[str]:
    """Intersect source columns with destination columns, safely.

    Only names present in the destination schema and matching the
    bare-identifier pattern survive, in source order. Hostile or
    unknown columns are dropped so one poisoned column cannot break
    or inject into the whole import.

    Args:
        src_columns: Column names read from the imported database.
        dest_columns: Column names of the destination table.

    Returns:
        Safe ordered subset of ``src_columns``.
    """
    dest = set(dest_columns)
    return [c for c in src_columns if c in dest and is_safe_identifier(c)]


def safe_extract_zip(archive: str | Path, dest: str | Path) -> list[str]:
    """Extract a zip archive with ZipSlip protection.

    Every member is validated before writing: absolute paths, parent
    references and symlink entries are skipped, and the resolved
    target must stay inside ``dest`` after symlink resolution.

    Args:
        archive: Path to the ``.zip`` file.
        dest: Directory receiving the extracted tree.

    Returns:
        Relative paths of the extracted members.
    """
    base = Path(dest)
    base.mkdir(parents=True, exist_ok=True)
    base_real = base.resolve()
    extracted: list[str] = []
    with zipfile.ZipFile(archive, "r") as zf:
        for info in zf.infolist():
            name = info.filename
            if not name or name.startswith("/") or name.startswith("\\"):
                continue
            if "\x00" in name:
                continue
            target = (base_real / name).resolve()
            try:
                target.relative_to(base_real)
            except ValueError:
                continue
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info, "r") as src, open(target, "wb") as fh:
                fh.write(src.read())
            extracted.append(str(target.relative_to(base_real)))
    return extracted


def safe_copy_tree(src: str | Path, dest: str | Path) -> int:
    """Copy a directory tree without symlink escape.

    Mirrors the campaign session-restore loop: symlinks are never
    followed, and every destination stays inside ``dest``.

    Args:
        src: Source directory.
        dest: Destination directory.

    Returns:
        Number of files copied.
    """
    base = Path(src)
    out = Path(dest)
    out.mkdir(parents=True, exist_ok=True)
    out_real = out.resolve()
    copied = 0
    for path in sorted(base.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        rel = path.relative_to(base)
        target = (out_real / rel).resolve()
        try:
            target.relative_to(out_real)
        except ValueError:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
        copied += 1
    return copied


__all__ = [
    "filter_columns",
    "is_safe_identifier",
    "safe_copy_tree",
    "safe_extract_zip",
]

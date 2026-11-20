"""Package the LazyOwn detection kit into a release tarball.

Collects the Sigma rules, Suricata rules and MISP event under
``detection_kit/`` and writes ``detection_kit/dist/lazyown_detection_kit_<version>.tar.gz``
plus a SHA-256 sidecar so release assets can be published verbatim.
"""

from __future__ import annotations

import hashlib
import tarfile
from pathlib import Path

KIT_DIRNAME = "detection_kit"
DIST_DIRNAME = "dist"
DEFAULT_VERSION = "1.0.0"
PACKED_MEMBERS = ("README.md", "sigma", "suricata", "misp")


def kit_root() -> Path:
    """Return the detection kit directory for this checkout."""
    return Path(KIT_DIRNAME)


def build(version: str = DEFAULT_VERSION) -> dict:
    """Pack the kit and return the artefact paths.

    Args:
        version: Release version stamped into the tarball name.

    Returns:
        Dict with ``archive`` and ``sha256`` paths, empty on failure.
    """
    root = kit_root()
    if not root.is_dir():
        return {"archive": "", "sha256": ""}
    dist = root / DIST_DIRNAME
    dist.mkdir(parents=True, exist_ok=True)
    archive = dist / f"lazyown_detection_kit_{version}.tar.gz"
    with tarfile.open(archive, "w:gz") as bundle:
        for member in PACKED_MEMBERS:
            candidate = root / member
            if candidate.exists():
                bundle.add(candidate, arcname=f"lazyown_detection_kit/{member}")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    sidecar = dist / f"lazyown_detection_kit_{version}.sha256"
    sidecar.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return {"archive": str(archive), "sha256": str(sidecar)}


if __name__ == "__main__":
    import sys

    chosen = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_VERSION
    result = build(chosen)
    print(result["archive"])

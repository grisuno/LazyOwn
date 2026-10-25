#!/usr/bin/env python3
"""Generate a minimal CycloneDX SBOM from the pinned requirements files.

Stdlib only, no network: parses ``requirements.txt`` (plus
``requirements-ml.txt`` with ``--with-ml``) and the project version from
``pyproject.toml``, and writes a CycloneDX 1.5 document.

Usage:
    python3 scripts/generate_sbom.py --out sbom.json
    python3 scripts/generate_sbom.py --with-ml --out sbom.json
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_requirement(line: str) -> tuple[str, str | None] | None:
    """Split one requirements line into (name, pinned_version|None)."""
    line = line.split("#", 1)[0].split(";", 1)[0].strip()
    if not line or line.startswith(("-", " ")):
        return None
    name = re.split(r"[<>=!~\s\[]", line, maxsplit=1)[0].strip()
    if not name:
        return None
    pinned = re.search(r"==\s*([A-Za-z0-9._\-+*]+)", line)
    return name, pinned.group(1) if pinned else None


def collect_components(with_ml: bool) -> list[dict]:
    """Parse requirements files into CycloneDX components, deduplicated."""
    files = [ROOT / "requirements.txt"]
    if with_ml:
        files.append(ROOT / "requirements-ml.txt")
    seen: dict[str, str | None] = {}
    for path in files:
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            parsed = parse_requirement(raw)
            if parsed is None:
                continue
            name, version = parsed
            if name not in seen:
                seen[name] = version
    components = []
    for name, version in sorted(seen.items()):
        bom_ref = f"pkg:pypi/{name}@{version}" if version else f"pkg:pypi/{name}"
        component: dict = {
            "type": "library",
            "bom-ref": bom_ref,
            "name": name,
            "purl": bom_ref,
        }
        if version:
            component["version"] = version
        components.append(component)
    return components


def project_version() -> str:
    """Read the package version from pyproject.toml."""
    match = re.search(r'^version\s*=\s*"([^"]+)"', (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.M)
    return match.group(1) if match else "0.0.0"


def build_sbom(with_ml: bool) -> dict:
    """Assemble the CycloneDX document."""
    components = collect_components(with_ml)
    digest = hashlib.sha256(json.dumps(components, sort_keys=True).encode("utf-8")).hexdigest()[:12]
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:lazyown-sbom-{digest}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "component": {"type": "application", "name": "lazyown", "version": project_version()},
            "tools": [{"name": "scripts/generate_sbom.py"}],
        },
        "components": components,
    }


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="sbom.json", help="output path")
    parser.add_argument("--with-ml", action="store_true", help="include requirements-ml.txt")
    args = parser.parse_args()
    document = build_sbom(with_ml=args.with_ml)
    Path(args.out).write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"SBOM: {len(document['components'])} components -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

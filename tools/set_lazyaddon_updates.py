"""Set or check the ``update`` flag on every lazyaddon YAML.

Usage:
    python3 tools/set_lazyaddon_updates.py            # set update: true
    python3 tools/set_lazyaddon_updates.py --check    # report only
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LAZYADDONS = ROOT / "lazyaddons"
UPDATE_RE = re.compile(r"^update\s*:\s*(.+)$")
ENABLED_RE = re.compile(r"^enabled\s*:")


def set_flag(path: Path, value: bool = True) -> bool:
    """Set the root update flag, returning True when the file changed."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    target = f"update: {'true' if value else 'false'}\n"
    for index, line in enumerate(lines):
        if UPDATE_RE.match(line.strip()):
            if line.strip() == target.strip():
                return False
            lines[index] = target
            path.write_text("".join(lines), encoding="utf-8")
            return True
    insert_at = None
    for index, line in enumerate(lines):
        if ENABLED_RE.match(line.strip()):
            insert_at = index + 1
            break
    if insert_at is None:
        insert_at = 1 if lines and lines[0].startswith("---") else 0
    lines.insert(insert_at, target)
    path.write_text("".join(lines), encoding="utf-8")
    return True


def read_flag(path: Path) -> bool | None:
    """Return the root update flag, or None when absent."""
    data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    if not isinstance(data, dict):
        return None
    if "update" not in data:
        return None
    return bool(data.get("update"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Set lazyaddon update flags")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--value", choices=("true", "false"), default="true")
    args = parser.parse_args()
    value = args.value == "true"
    changed = missing = 0
    bad: list[str] = []
    for path in sorted(LAZYADDONS.glob("*.yaml")):
        try:
            current = read_flag(path)
        except Exception as exc:
            bad.append(f"{path.name}: {exc}")
            continue
        if current is None:
            missing += 1
        if args.check:
            if current is not value:
                print(f"{path.name}: update={current}")
            continue
        if current is not value:
            if set_flag(path, value):
                changed += 1
    if bad:
        for item in bad:
            print(f"INVALID {item}")
        raise SystemExit(1)
    if args.check:
        print(f"missing={missing}")
        raise SystemExit(0 if missing == 0 else 1)
    print(f"changed={changed} total={len(list(LAZYADDONS.glob('*.yaml')))}")


if __name__ == "__main__":
    main()

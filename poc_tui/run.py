"""Convenience launcher that symlinks LazyOwn dirs and starts the TUI."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    poc_dir = Path(__file__).parent
    repo_dir = poc_dir.parent  # LazyOwn root

    # Create symlinks to LazyOwn dirs if they don't exist locally
    for dirname in ("lazyaddons", "plugins", "tools"):
        local = poc_dir / dirname
        target = repo_dir / dirname
        if not local.exists() and target.is_dir():
            local.symlink_to(target)
            print(f"[*] Symlinked {dirname}/ -> {target}")

    # Create a default payload.json if missing
    payload = poc_dir / "payload.json"
    if not payload.exists():
        payload.write_text(
            '{\n  "rhost": "",\n  "lhost": "",\n  "lport": "4444",\n  "domain": "",\n  "rport": "80"\n}',
            encoding="utf-8",
        )
        print("[*] Created default payload.json")

    os.chdir(poc_dir)

    from app import main as run_app
    run_app()


if __name__ == "__main__":
    main()

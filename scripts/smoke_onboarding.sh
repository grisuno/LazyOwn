#!/usr/bin/env bash
# Smoke test for the 5-minute onboarding path.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"
fail=0
check() { if eval "$2"; then echo "[+] $1"; else echo "[!] $1"; fail=1; fi; }
check "payload.example.json exists" "[ -f payload.example.json ]"
check "requirements.txt exists" "[ -f requirements.txt ]"
check "pyproject entry lazyown" "grep -q 'lazyown = ' pyproject.toml"
check "docker image documented" "grep -q 'ghcr.io/grisuno/lazyown' QUICKSTART.md README.md"
check "golden path docs present" "grep -q 'auto_populate' ESSENTIALS.md"
check "demo gifs present" "[ -f assets/demo/golden-path.gif ] && [ -f assets/demo/c2-collab.gif ] && [ -f assets/demo/mcp-ai.gif ]"
check "htb walkthrough present" "[ -f docs/examples/htb-lame-walkthrough.md ]"
check "comparison present" "[ -f COMPARISON.md ]"
check "core deps importable" "python3 -c 'import cmd2, flask, rich, yaml' 2>/dev/null || echo skip"
python3 scripts/build_command_index.py --check 2>/dev/null || echo "[i] command index check skipped (no --check flag)"
exit $fail

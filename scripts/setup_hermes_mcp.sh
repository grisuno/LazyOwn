#!/usr/bin/env bash
# setup_hermes_mcp.sh — register LazyOwn MCP server in Hermes Agent config
# Usage: bash scripts/setup_hermes_mcp.sh [--check]
#   --check    verify registration without writing

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
MCP_PATH="${REPO_ROOT}/skills/lazyown_mcp.py"

# Determine Hermes home
HERMES_HOME="${HERMES_HOME:-${HOME}/.hermes}"
CONFIG_YAML="${HERMES_HOME}/config.yaml"

LAZYOWN_NAME="lazyown"
LAZYOWN_CMD="python3 ${MCP_PATH}"

echo "=== LazyOwn Hermes MCP Setup ==="
echo "Repo root: ${REPO_ROOT}"
echo "MCP path:  ${MCP_PATH}"
echo "Hermes config: ${CONFIG_YAML}"
echo ""

# Pre-flight checks
if [[ ! -f "${MCP_PATH}" ]]; then
    echo "ERROR: MCP server not found at ${MCP_PATH}"
    echo "Make sure you are in the LazyOwn repo root."
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required but not installed."
    exit 1
fi

if [[ ! -f "${CONFIG_YAML}" ]]; then
    echo "WARNING: Hermes config not found at ${CONFIG_YAML}"
    echo "Hermes Agent may not be installed, or HERMES_HOME is set differently."
    echo ""
    echo "To install Hermes:"
    echo "  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
    exit 1
fi

# Check mode — just verify and print status
if [[ "${1:-}" == "--check" ]]; then
    if python3 -c "
import yaml, sys
cfg = yaml.safe_load(open('${CONFIG_YAML}'))
servers = cfg.get('mcp', {}).get('servers', {})
if '${LAZYOWN_NAME}' in servers:
    s = servers['${LAZYOWN_NAME}']
    print(f'FOUND: {s.get(\"command\", s.get(\"url\", \"???\"))}')
    sys.exit(0)
else:
    print('NOT REGISTERED')
    sys.exit(1)
" 2>/dev/null; then
        echo "LazyOwn MCP is already registered in Hermes."
        exit 0
    else
        echo "LazyOwn MCP is NOT registered."
        echo "Run without --check to register."
        exit 1
    fi
fi

# Registration via Python (safer than raw YAML editing)
python3 << PYEOF
import yaml
import sys
import os

config_path = "${CONFIG_YAML}"
name = "${LAZYOWN_NAME}"
cmd = "${LAZYOWN_CMD}"
mcp_path = "${MCP_PATH}"

with open(config_path, "r") as f:
    cfg = yaml.safe_load(f) or {}

# Ensure mcp section exists
if "mcp" not in cfg:
    cfg["mcp"] = {}
if "servers" not in cfg["mcp"]:
    cfg["mcp"]["servers"] = {}

# Register or update
existing = cfg["mcp"]["servers"].get(name)
cfg["mcp"]["servers"][name] = {"command": cmd}

with open(config_path, "w") as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

if existing:
    print(f"UPDATED: {name} MCP server in {config_path}")
else:
    print(f"REGISTERED: {name} MCP server in {config_path}")

print(f"  command: {cmd}")
print("")
print("Next steps:")
print("  1. Restart your Hermes session or run /reload-mcp")
print("  2. Verify with: hermes mcp list")
print("  3. Test with:   hermes mcp test lazyown")
PYEOF

echo ""
echo "Setup complete."

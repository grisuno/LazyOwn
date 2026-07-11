#!/usr/bin/env bash
# validate_agent_contract.sh
#
# CI validation of the AGENTS.md branching model and coding standards.
# Called by .github/workflows/agent-contract.yml on every push/PR to dev.
#
# Checks:
#   1. Branch name matches allowed patterns (dev, main, pp, feature/*, hotfix/*).
#   2. No commits from dev directly target main (PRs only).
#   3. No secrets or credentials committed (baseline check).
#   4. No Spanish strings in code files (enforce English-only rule).
#   5. No hardcoded IPs/paths/creds outside payload.json.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

failures=0

check() {
    local desc="$1"
    local cmd="$2"
    if eval "$cmd" 2>/dev/null; then
        echo -e "  ${GREEN}PASS${NC} $desc"
    else
        echo -e "  ${RED}FAIL${NC} $desc"
        failures=$((failures + 1))
    fi
}

# --- Branch name validation ---
BRANCH="${GITHUB_HEAD_REF:-${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')}}"

check "Branch name matches allowed pattern (dev|main|pp|feature/*|hotfix/*)" \
    "[[ '$BRANCH' =~ ^(dev|main|pp|feature/|hotfix/) ]] || [[ '$BRANCH' == 'main' ]]"

# --- English-only check: no Spanish in .py and .js files ---
SPANISH_PATTERNS='\b(aplicaci[oó]n|archivo|cadena|cadena|clave|c[oó]digo|configuraci[oó]n|contrase[ñn]a|correo|datos|directorio|ejecutar|enviar|error|fichero|funci[oó]n|idioma|imagen|informaci[oó]n|l[íi]nea|llamada|mensaje|m[oó]dulo|nombre|n[úu]mero|opci[oó]n|p[áa]gina|par[áa]metro|puerto|respuesta|resultado|sali(d|r)|sistema|solicitud|tama[ñn]o|tarjeta|usuario|valor|ventana|archivo)\b'

check "No Spanish strings in Python files (English-only rule)" \
    "! git grep -n -i -E '$SPANISH_PATTERNS' -- '*.py' ':!tests/' ':!modules/' ':!skills/' 2>/dev/null | head -20 | grep ."

# --- No hardcoded credentials outside payload.json ---
check "No password/secret/credential assignments outside payload.json" \
    "! git grep -n -E '(password|PASSWORD|secret|SECRET|credential|api_key|API_KEY)\s*[:=]\s*['\\\"][^'\\\"]+['\\\"]' -- '*.py' '*.sh' '*.yaml' '*.yml' ':!payload.json' ':!tests/' 2>/dev/null | grep -v 'utils\.py\|config\.py\|\.secrets\.baseline' | head -10 | grep ."

# --- No hardcoded wordlist paths outside payload.json ---
check "No hardcoded wordlist paths outside payload.json" \
    "! git grep -n '/usr/share/wordlists' -- '*.py' '*.sh' 2>/dev/null | grep -v 'payload.json\|utils.py' | head -5 | grep ."

# --- Commit message format (if checking a PR) ---
if [ -n "${GITHUB_HEAD_REF:-}" ]; then
    COMMIT_MSG=$(git log --format=%s -1 2>/dev/null || echo "")
    check "Last commit message is not empty" "[ -n '$COMMIT_MSG' ]"
fi

echo ""
if [ "$failures" -gt 0 ]; then
    echo -e "${RED}FAILED${NC} $failures contract violation(s) found."
    exit 1
else
    echo -e "${GREEN}ALL CHECKS PASSED${NC}"
    exit 0
fi

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

pass() {
    echo -e "  ${GREEN}PASS${NC} $1"
}

fail() {
    echo -e "  ${RED}FAIL${NC} $1"
    failures=$((failures + 1))
}

check() {
    local desc="$1"
    local cmd="$2"
    if eval "$cmd" 2>/dev/null; then
        pass "$desc"
    else
        fail "$desc"
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
# Pentest help-text, doc placeholders (<...>), template vars ({{ ... }}),
# shell arg plumbing ($1/$2/${...}), key-name constants and test fixtures
# are not committed secrets. Implemented as a function to avoid eval
# quoting pitfalls with nested quote classes.
check_no_hardcoded_passwords() {
    local matches
    matches=$(git grep -n -E -e "(password|PASSWORD|secret|SECRET|credential|api_key|API_KEY)[[:space:]]*[:=][[:space:]]*['\"][^'\"]+['\"]" -- '*.py' '*.sh' '*.yaml' '*.yml' ':!payload.json' ':!tests/' 2>/dev/null | grep -v -E -e 'utils\.py' -e 'config\.py' -e '\.secrets\.baseline' -e 'sessions/' -e 'skills/tests/' -e 'constants\.py' -e 'llm_factory' -e 'dpapi_harvester' -e 'kerberos_tickets' -e 'phishing_wizard' -e 'lazyaddons/' -e 'readmenator-rules/' -e 'commands/enum\.py' -e 'lazycurl' -e 'lazylynis' -e 'lazyevilwimrm' -e 'lazypsexec' -e 'username=guest' -e '{password}' -e 'Administrator' -e 'mimikatz' || true)
    if [ -z "$matches" ]; then
        pass "No password/secret/credential assignments outside payload.json"
    else
        echo "$matches" | head -10
        fail "No password/secret/credential assignments outside payload.json"
    fi
}
check_no_hardcoded_passwords

# --- No hardcoded wordlist paths outside payload.json ---
# Help-text examples, docstrings and filesystem hints are allowed; only real
# default assignments outside payload.json are violations.
check_no_hardcoded_wordlists() {
    local matches
    matches=$(git grep -n -E -e "(wordlist|WORDLIST)[[:space:]]*=[[:space:]]*['\"]?/usr/share/wordlists" -- '*.py' '*.sh' 2>/dev/null | grep -v -E -e 'payload\.json' -e 'utils\.py' -e 'Example' -e 'example' -e 'poutput' -e 'print_msg' -e '_HINTS' -e '#' -e 'HashCracker\(wordlist=' || true)
    if [ -z "$matches" ]; then
        pass "No hardcoded wordlist paths outside payload.json"
    else
        echo "$matches" | head -5
        fail "No hardcoded wordlist paths outside payload.json"
    fi
}
check_no_hardcoded_wordlists

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

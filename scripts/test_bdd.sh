#!/usr/bin/env bash
# Behavior-driven (BDD) suite gate for LazyOwn.
#
# Every BDD scenario lives in a pytest module whose tests state the Given,
# When, Then contract in the docstring. This gate runs those modules, scoped to
# the files a change touched so the loop stays fast, with an --all mode for the
# full run at the end of a work unit.
#
# Modes:
#   scripts/test_bdd.sh                 changed BDD modules vs HEAD
#   scripts/test_bdd.sh --all           every test module that declares BDD
#   scripts/test_bdd.sh --list          print the BDD modules
#   scripts/test_bdd.sh FILE [FILE ...] explicit test files
#
# Environment:
#   PYTHON        interpreter for pytest (default: env/bin/python3)
#   PYTEST_ARGS   extra pytest arguments
#   TIMEOUT       suite timeout in seconds (default: 3600)
#   FAIL_FAST     when 1, stop at the first failing test

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE}/.." && pwd)"
PYTHON="${PYTHON:-${REPO_ROOT}/env/bin/python3}"
if [ ! -x "${PYTHON}" ]; then
    PYTHON="python3"
fi
TIMEOUT="${TIMEOUT:-3600}"
FAIL_FAST="${FAIL_FAST:-0}"
PYTEST_ARGS="${PYTEST_ARGS:-}"

bdd_modules() {
    grep -l -E "\bBDD\b" "${REPO_ROOT}"/tests/test_*.py 2>/dev/null | sort
}

changed_tests() {
    {
        git -C "${REPO_ROOT}" diff --name-only HEAD 2>/dev/null
        git -C "${REPO_ROOT}" ls-files --others --exclude-standard 2>/dev/null
    } | grep -E '^tests/test_.*\.py$' | sort -u
}

MODE="scoped"
TARGETS=()
for arg in "$@"; do
    case "${arg}" in
        --all) MODE="all" ;;
        --list)
            bdd_modules | while read -r module; do echo "${module#"${REPO_ROOT}"/}"; done
            exit 0
            ;;
        --help | -h)
            sed -n '2,20p' "${BASH_SOURCE[0]}"
            exit 0
            ;;
        *)
            TARGETS+=("${arg}")
            MODE="explicit"
            ;;
    esac
done

if [ "${MODE}" = "all" ]; then
    while read -r module; do
        TARGETS+=("${module}")
    done < <(bdd_modules)
elif [ "${MODE}" = "scoped" ]; then
    while read -r module; do
        [ -n "${module}" ] && TARGETS+=("${REPO_ROOT}/${module}")
    done < <(changed_tests)
fi

if [ "${#TARGETS[@]}" -eq 0 ]; then
    echo "[bdd] no changed BDD modules; nothing to run"
    exit 0
fi

EXTRA=()
if [ "${FAIL_FAST}" = "1" ]; then
    EXTRA+=("-x")
fi

echo "=== LazyOwn BDD gate: ${#TARGETS[@]} module(s) ==="
for target in "${TARGETS[@]}"; do echo "  ${target#"${REPO_ROOT}"/}"; done
echo ""

cd "${REPO_ROOT}" || exit 2
# shellcheck disable=SC2086
timeout "${TIMEOUT}" "${PYTHON}" -m pytest -q -p no:cacheprovider "${EXTRA[@]}" ${PYTEST_ARGS} "${TARGETS[@]}"
STATUS=$?

if [ "${STATUS}" -eq 0 ]; then
    echo ""
    echo "=== BDD summary: all modules passed ==="
    exit 0
fi
echo ""
echo "=== BDD summary: failed (pytest exit ${STATUS}) ==="
exit "${STATUS}"

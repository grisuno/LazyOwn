#!/usr/bin/env bash
# Mutation gate for LazyOwn.
#
# The gate runs the curated mutation runners under tests/. Each runner mutates
# one production module and asserts the matching test suite kills the mutant.
# A surviving mutant means the suite does not cover the behaviour, and the gate
# fails so the gap is closed before the change lands.
#
# Modes:
#   scripts/mutate.sh                    scoped to source files changed vs HEAD
#   scripts/mutate.sh --all              every curated runner
#   scripts/mutate.sh --list             print the available runners
#   scripts/mutate.sh FILE [FILE ...]    runners that reference the given files
#
# Environment:
#   PYTHON             interpreter for the runners (default: env/bin/python3)
#   MUTATION_TIMEOUT   per runner timeout in seconds (default: 1800)

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE}/.." && pwd)"
PYTHON="${PYTHON:-${REPO_ROOT}/env/bin/python3}"
if [ ! -x "${PYTHON}" ]; then
    PYTHON="python3"
fi
TIMEOUT="${MUTATION_TIMEOUT:-1800}"

runners() {
    ls "${REPO_ROOT}"/tests/run_mutation_*.py 2>/dev/null | sort
}

changed_sources() {
    {
        git -C "${REPO_ROOT}" diff --name-only HEAD 2>/dev/null
        git -C "${REPO_ROOT}" ls-files --others --exclude-standard 2>/dev/null
    } | grep -E '\.py$' | grep -E '^(core|modules|cli|lazyc2)/|^lazyown\.py$|^lazyc2\.py$' | sort -u
}

usage() {
    sed -n '2,18p' "${BASH_SOURCE[0]}"
}

MODE="scoped"
TARGETS=()
for arg in "$@"; do
    case "${arg}" in
        --all) MODE="all" ;;
        --list)
            runners | while read -r runner; do echo "${runner#"${REPO_ROOT}"/}"; done
            exit 0
            ;;
        --help | -h)
            usage
            exit 0
            ;;
        *)
            TARGETS+=("${arg}")
            MODE="explicit"
            ;;
    esac
done

if [ "${MODE}" = "explicit" ]; then
    :
elif [ "${MODE}" = "scoped" ]; then
    while read -r source; do
        [ -n "${source}" ] && TARGETS+=("${source}")
    done < <(changed_sources)
fi

SELECTED=()
if [ "${MODE}" = "all" ]; then
    while read -r runner; do
        SELECTED+=("${runner}")
    done < <(runners)
else
    if [ "${#TARGETS[@]}" -eq 0 ]; then
        echo "[mutate] no changed source files; nothing to mutate"
        exit 0
    fi
    for target in "${TARGETS[@]}"; do
        normalized="${target#"${REPO_ROOT}"/}"
        while read -r match; do
            [ -z "${match}" ] && continue
            already=0
            for seen in "${SELECTED[@]:-}"; do
                [ "${seen}" = "${match}" ] && already=1 && break
            done
            [ "${already}" -eq 0 ] && SELECTED+=("${match}")
        done < <(grep -l -F "${normalized}" "${REPO_ROOT}"/tests/run_mutation_*.py 2>/dev/null || true)
    done
fi

if [ "${#SELECTED[@]}" -eq 0 ]; then
    echo "[mutate] no curated runner references the target files:"
    for target in "${TARGETS[@]}"; do echo "  ${target}"; done
    echo "[mutate] add a tests/run_mutation_<contract>.py runner for this change"
    exit 0
fi

echo "=== LazyOwn mutation gate: ${#SELECTED[@]} runner(s) ==="
FAIL=0
for runner in "${SELECTED[@]}"; do
    name="$(basename "${runner}")"
    echo "--- ${name}"
    output="$(cd "${REPO_ROOT}" && timeout "${TIMEOUT}" "${PYTHON}" "${runner}" 2>&1)"
    status=$?
    printf '%s\n' "${output}"
    if [ "${status}" -ne 0 ] || printf '%s\n' "${output}" | grep -q "SURVIVED"; then
        echo "    FAIL ${name}"
        FAIL=$((FAIL + 1))
    else
        echo "    PASS ${name}"
    fi
done

echo ""
echo "=== mutation summary: ${#SELECTED[@]} runner(s), ${FAIL} failed ==="
if [ "${FAIL}" -gt 0 ]; then
    echo "A surviving mutant means the suite does not cover that behaviour."
    exit 1
fi
exit 0

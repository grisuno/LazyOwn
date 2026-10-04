# modules

*Community 11 | 72 files | cohesion 0.45*

## Definition

This community groups 72 file(s) rooted at `modules` with dominant language py (cohesion 0.45). Central symbols: `ACIEngine`, `ACIGoal`, `ACIPlan`, `ACIPlanner`, `ACIReflector`, `ActionCategory`, `AgentBridgeWorker`, `AgentTool`. Core file: `skills/autonomous_daemon.py` (132 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: LazyOwn HoneyPot  ██╗   .

## Files

### `modules` (27 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_tool.py` | py | utility | 4 | no |
| `modules/c2_profile.py` | py | utility | 32 | yes |

### `tests` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aci_planner.py` | py | testing | 95 | yes |
| `tests/test_autonomous_replay.py` | py | testing | 18 | yes |

### `skills` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/aci_planner.py` | py | utility | 42 | yes |
| `skills/autonomous_daemon.py` | py | presentation | 132 | yes |

### `contrib/legacy` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyhoneypot.py` | py | utility | 15 | yes |
| `contrib/legacy/lazyopenssh77enum2.py` | py | utility | 5 | yes |

### `lazygui/config` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/config/__init__.py` | py | presentation | 0 | yes |
| `lazygui/config/c2_credentials.py` | py | presentation | 4 | yes |

### `lazygui/services` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/services/__init__.py` | py | presentation | 0 | yes |
| `lazygui/services/factory.py` | py | presentation | 4 | yes |

### `core` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/logging.py` | py | infrastructure | 12 | yes |
| `core/scheduler.py` | py | infrastructure | 17 | yes |

### `lazygui` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/__main__.py` | py | presentation | 1 | yes |
| `lazygui/app.py` | py | presentation | 14 | yes |

### `modules/integrations` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/nuclei_bridge.py` | py | utility | 29 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazy_sentinel4.py` | py | utility | 47 | no |

### `lazygui/windows` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/windows/connect_dialog.py` | py | presentation | 9 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_autonomous_daemon.py` | py | testing | 88 | yes |

*... and 52 more files in this community.*


## Key Symbols

- `parse_args` (function, `contrib/legacy/lazyhoneypot.py:34`) `def parse_args()`
- `setup_logging` (function, `contrib/legacy/lazyhoneypot.py:52`) `def setup_logging(log_file)`
- `generate_rsa_key` (function, `contrib/legacy/lazyhoneypot.py:56`) `def generate_rsa_key(key_filename)`
- `Server` (class, `contrib/legacy/lazyhoneypot.py:60`) `class Server(ServerInterface)`
- `__init__` (method, `contrib/legacy/lazyhoneypot.py:61`) `def __init__(self)`
- `check_channel_request` (method, `contrib/legacy/lazyhoneypot.py:64`) `def check_channel_request(self, kind, chanid)`
- `check_auth_password` (method, `contrib/legacy/lazyhoneypot.py:69`) `def check_auth_password(self, username, password)`
- `handle_connection` (method, `contrib/legacy/lazyhoneypot.py:74`) `def handle_connection(client_socket, host_key, commands_log, downloads_log, down`
- `handle_file_download` (method, `contrib/legacy/lazyhoneypot.py:110`) `def handle_file_download(command, downloads_dir, downloads_log)`
- `log_command` (method, `contrib/legacy/lazyhoneypot.py:128`) `def log_command(command, commands_log)`
- `log_downloaded_file` (method, `contrib/legacy/lazyhoneypot.py:132`) `def log_downloaded_file(filename, url, downloads_log)`
- `analyze_traffic` (method, `contrib/legacy/lazyhoneypot.py:136`) `def analyze_traffic()`
- `process_packet` (method, `contrib/legacy/lazyhoneypot.py:137`) `def process_packet(packet)`
- `alert_admin` (method, `contrib/legacy/lazyhoneypot.py:147`) `def alert_admin(message)`
- `main` (method, `contrib/legacy/lazyhoneypot.py:165`) `def main()`
- `InvalidUsername` (class, `contrib/legacy/lazyopenssh77enum2.py:14`) `class InvalidUsername(Exception)`
- `add_boolean` (method, `contrib/legacy/lazyopenssh77enum2.py:19`) `def add_boolean()`
- `service_accept` (method, `contrib/legacy/lazyopenssh77enum2.py:30`) `def service_accept()`
- `invalid_username` (method, `contrib/legacy/lazyopenssh77enum2.py:36`) `def invalid_username()`
- `check_user` (method, `contrib/legacy/lazyopenssh77enum2.py:50`) `def check_user(username)`
- `signal_handler` (function, `contrib/legacy/lazysearch_bot.py:59`) `def signal_handler(sig, frame)`
- `show_help` (function, `contrib/legacy/lazysearch_bot.py:65`) `def show_help(message)`
- `check_api_key` (function, `contrib/legacy/lazysearch_bot.py:69`) `def check_api_key()`
- `configure_logging` (function, `contrib/legacy/lazysearch_bot.py:75`) `def configure_logging(debug)`
- `parse_args` (function, `contrib/legacy/lazysearch_bot.py:79`) `def parse_args()`
- `create_complex_prompt` (function, `contrib/legacy/lazysearch_bot.py:86`) `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
- `execute_command` (function, `contrib/legacy/lazysearch_bot.py:109`) `def execute_command(command)`
- `load_knowledge_base` (function, `contrib/legacy/lazysearch_bot.py:112`) `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function, `contrib/legacy/lazysearch_bot.py:118`) `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function, `contrib/legacy/lazysearch_bot.py:122`) `def add_to_knowledge_base(prompt, command, file_path)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 395
- Cross-boundary resolved imports (EXTRACTED): 245

## Connections

- [EXTRACTED] depends_on community 3 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 0 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 1 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/session_resumer.py imports core/logging.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- [cycle] `modules/detection_oracle.py` -> `modules/detection_feed.py` -> `modules/detection_oracle.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`

## Open Questions

- Why do 7 file(s) lack file-level docs (e.g. `contrib/legacy/lazyssh.py`)? What purpose do they serve?
- Can the cycle `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` be broken with an interface?
- What would break if the most connected file in modules changed?
- Should modules be split, given cohesion 0.45?

## Sources

- `contrib/legacy/lazyhoneypot.py`
- `contrib/legacy/lazyopenssh77enum2.py`
- `contrib/legacy/lazysearch_bot.py`
- `contrib/legacy/lazyssh.py`
- `core/logging.py`
- `core/scheduler.py`
- `core/security.py`
- `lazy_sentinel4.py`
- `lazygui/__main__.py`
- `lazygui/app.py`
- `lazygui/config/__init__.py`
- `lazygui/config/c2_credentials.py`
- `lazygui/config/paths.py`
- `lazygui/config/settings.py`
- `lazygui/services/__init__.py`
- `lazygui/services/factory.py`
- `lazygui/services/local_backend.py`
- `lazygui/services/teamserver_backend.py`
- `lazygui/windows/connect_dialog.py`
- `modules/agent_tool.py`
- *... and 52 more*

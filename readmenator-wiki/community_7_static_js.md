# static/js

*Community 7 | 26 files | cohesion 0.52*

## Definition

This community groups 26 file(s) rooted at `static/js` with dominant language js (cohesion 0.52). Central symbols: `A`, `As`, `B`, `BUFFER`, `BackgroundSize`, `Be`, `BezierCurve`, `Bk`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

### `static/js` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |
| `static/js/chart.min.js` | js | utility | 88 | yes |
| `static/js/force-graph-1.43.5.min.js` | js | utility | 31 | yes |
| `static/js/html2pdf.bundle.min.js` | js | utility | 738 | no |
| `static/js/jquery-3.5.1.slim.min.js` | js | utility | 6 | yes |
| `static/js/particles.js` | js | utility | 11 | yes |

### `cli` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/show.py` | py | utility | 1 | yes |
| `cli/style.py` | py | utility | 4 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/process.py` | py | business_logic | 12 | yes |
| `core/prompt.py` | py | utility | 8 | yes |

### `modules` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/exp.c` | c | utility | 58 | yes |
| `modules/search.py` | py | utility | 0 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazybinenc.py` | py | utility | 2 | no |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/state.py` | py | utility | 0 | yes |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_cli_assign.py` | py | testing | 36 | yes |

*... and 6 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:36`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `format_payload` (function, `cli/show.py:14`) `def format_payload(params)` - Render ``params`` as a sorted, aligned ``key = value`` block.
- `style` (function, `cli/style.py:49`) `def style(token, theme)` - Return the Rich style string for a semantic token.
- `active_tokens` (function, `cli/style.py:68`) `def active_tokens(payload)` - Resolve every :data:`TOKEN_KEYS` entry for the payload's theme.
- `paint` (function, `cli/style.py:84`) `def paint(text, token, payload)` - Render ``text`` with the style of ``token`` for the active theme.
- `render_prompt` (function, `cli/style.py:98`) `def render_prompt(console, segments, payload)` - Print a themed prompt line composed of ``(text, token)`` pairs.
- `generate_key_iv` (function, `contrib/legacy/lazybinenc.py:12`) `def generate_key_iv(sessions_path)`
- `main` (function, `contrib/legacy/lazybinenc.py:54`) `def main()`
- `check_go_tool_installed` (function, `core/process.py:34`) `def check_go_tool_installed(tool_name)` - Check if a Go tool binary is installed and runnable.
- `is_binary_present` (function, `core/process.py:54`) `def is_binary_present(binary_name)` - Check whether binary is on ``PATH``.
- `handle_multiple_rhosts` (function, `core/process.py:68`) `def handle_multiple_rhosts(func)` - Decorator that iterates over a list of remote hosts.
- `wrapper` (function, `core/process.py:82`) `def wrapper(self)`
- `check_sudo` (function, `core/process.py:97`) `def check_sudo()` - Re-launch the script with ``sudo`` if not already root.
- `run` (function, `core/process.py:108`) `def run(command)` - Execute a shell command via ``SafeRunner``.
- `is_package_installed` (function, `core/process.py:143`) `def is_package_installed(package_name)` - Check whether a Python package is importable.
- `_print_run_command_status` (function, `core/process.py:159`) `def _print_run_command_status(command, elapsed, exit_code)` - Print a dim completion line (elapsed time + exit code) after a run.
- `run_command` (function, `core/process.py:183`) `def run_command(command, timeout)` - Run a command, streaming output in real time.
- `_drain_stderr` (function, `core/process.py:220`) `def _drain_stderr()`
- `ensure_tmux_session` (function, `core/process.py:253`) `def ensure_tmux_session(session_name)` - Create a tmux session if it does not already exist.
- `activate_server` (function, `core/process.py:271`) `def activate_server(httpd, url, lhost)` - Start an HTTP server and print the serving URL.
- `_load_prompt_payload` (function, `core/prompt.py:17`) `def _load_prompt_payload()` - Load ``payload.json`` and return a dict with default values.
- `get_git_info` (function, `core/prompt.py:35`) `def get_git_info()` - Return current git branch and dirty-status for the prompt.
- `get_venv_info` (function, `core/prompt.py:60`) `def get_venv_info()` - Return the active virtualenv name, or empty string if none.
- `get_kernel` (function, `core/prompt.py:68`) `def get_kernel()` - Return the running kernel version (short form).
- `get_terminal_size` (function, `core/prompt.py:78`) `def get_terminal_size()` - Return ``(width, height)`` of the terminal, defaulting to 80x24.
- `get_local_ips` (function, `core/prompt.py:87`) `def get_local_ips()` - Return a comma-separated string of non-loopback IPv4 addresses.
- `copy2clip` (function, `core/prompt.py:109`) `def copy2clip(text)` - Copy ``text`` to the system clipboard via xclip.
- `getprompt` (function, `core/prompt.py:127`) `def getprompt()` - Build the coloured status line for the CLI header and C2 dashboard.
- `main` (function, `key.py:10`) `def main()`
- `_GNU_SOURCE` (macro, `modules/exp.c:2`) `#define _GNU_SOURCE`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 241
- Cross-boundary resolved imports (EXTRACTED): 45

## Connections

- [EXTRACTED] depends_on community 7 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 3 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports cli/assign.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/process.py` via `subprocess` (5 hops)
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:371` `set_stable_table_and_set` `seq`: `seq` assigned at line 371 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:356` `set_stable_table_and_set` `table_seq`: `table_seq` assigned at line 356 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:406` `set_trigger_set_and_overwrite` `exprid`: `exprid` assigned at line 406 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:423` `set_trigger_set_and_overwrite` `seq`: `seq` assigned at line 423 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:453` `spray_mqueue` `unresolved`: `unresolved` assigned at line 453 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:455` `spray_mqueue` `priority`: `priority` assigned at line 455 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:465` `gather_mqueue` `priority`: `priority` assigned at line 465 but never read afterwards.

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `contrib/legacy/lazybinenc.py`)? What purpose do they serve?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.52?

## Sources

- `cli/assign.py`
- `cli/show.py`
- `cli/style.py`
- `contrib/legacy/lazybinenc.py`
- `core/process.py`
- `core/prompt.py`
- `key.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/exp.c`
- `modules/search.py`
- `static/js/3d-force-graph-1.73.4.min.js`
- `static/js/bootstrap-4.5.2.min.js`
- `static/js/bootstrap-5.3.0.bundle.min.js`
- `static/js/chart.min.js`
- `static/js/force-graph-1.43.5.min.js`
- `static/js/html2pdf.bundle.min.js`
- `static/js/jquery-3.5.1.slim.min.js`
- `static/js/particles.js`
- `static/js/popper-2.5.4.min.js`
- *... and 6 more*

# static/js

*Community 9 | 62 files | cohesion 0.46*

## Definition

This community groups 62 file(s) rooted at `static/js` with dominant language py (cohesion 0.46). Central symbols: `A`, `As`, `B`, `BUFFER`, `BackgroundSize`, `Be`, `BezierCurve`, `Bk`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ! jQuery v1.11.3 | (c) 2005, 2015 jQuery Foundation, Inc. | jquery.org/license.

## Files

### `static/js` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |

### `tests` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_crypto.py` | py | testing | 22 | yes |
| `tests/test_cli_assign.py` | py | testing | 44 | yes |

### `modules` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/command_executor.py` | py | utility | 24 | yes |
| `modules/dns_beacon.py` | py | utility | 19 | yes |

### `cli` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/session_resumer.py` | py | utility | 6 | yes |

### `core` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/process.py` | py | business_logic | 12 | yes |

### `poc_tui` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | utility | 0 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/mcp_bridge.py` | py | utility | 20 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `2026-11-19_154944` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `2026-11-19_154944/jquery-1.11.3.min.js` | js | utility | 3 | yes |

### `2026-11-19_162254` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `2026-11-19_162254/jquery-1.11.3.min.js` | js | utility | 3 | yes |

### `2026-11-19_164345` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `2026-11-19_164345/jquery-1.11.3.min.js` | js | utility | 3 | yes |

### `2026-11-19_170839` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `2026-11-19_170839/jquery-1.11.3.min.js` | js | utility | 3 | yes |

### `gyms/docker/php2shell/src` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `gyms/docker/php2shell/src/info.php` | php | utility | 0 | no |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/state.py` | py | utility | 0 | yes |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `static/hexabot` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/hexabot/hexabot-spinner.js` | js | utility | 24 | no |

*... and 42 more files in this community.*


## Key Symbols

- `s` (function, `2026-11-19_154944/jquery-1.11.3.min.js:2`) - /*! jQuery v1.11.3 \| (c) 2005, 2015 jQuery Foundation, Inc. \| jquery.org/license
- `c` (function, `2026-11-19_154944/jquery-1.11.3.min.js:4`)
- `d` (function, `2026-11-19_154944/jquery-1.11.3.min.js:5`)
- `s` (function, `2026-11-19_162254/jquery-1.11.3.min.js:2`) - /*! jQuery v1.11.3 \| (c) 2005, 2015 jQuery Foundation, Inc. \| jquery.org/license
- `c` (function, `2026-11-19_162254/jquery-1.11.3.min.js:4`)
- `d` (function, `2026-11-19_162254/jquery-1.11.3.min.js:5`)
- `s` (function, `2026-11-19_164345/jquery-1.11.3.min.js:2`) - /*! jQuery v1.11.3 \| (c) 2005, 2015 jQuery Foundation, Inc. \| jquery.org/license
- `c` (function, `2026-11-19_164345/jquery-1.11.3.min.js:4`)
- `d` (function, `2026-11-19_164345/jquery-1.11.3.min.js:5`)
- `s` (function, `2026-11-19_170839/jquery-1.11.3.min.js:2`) - /*! jQuery v1.11.3 \| (c) 2005, 2015 jQuery Foundation, Inc. \| jquery.org/license
- `c` (function, `2026-11-19_170839/jquery-1.11.3.min.js:4`)
- `d` (function, `2026-11-19_170839/jquery-1.11.3.min.js:5`)
- `apply_assign` (function, `cli/assign.py:42`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `_build_auto_populate_parser` (function, `cli/commands/mcp_bridge.py:55`) `def _build_auto_populate_parser()` - Return the argparse parser used by ``auto_populate``.
- `_build_facts_show_parser` (function, `cli/commands/mcp_bridge.py:72`) `def _build_facts_show_parser()` - Return the argparse parser used by ``facts_show``.
- `_build_rag_query_parser` (function, `cli/commands/mcp_bridge.py:89`) `def _build_rag_query_parser()` - Return the argparse parser used by ``rag_query``.
- `_build_parquet_query_parser` (function, `cli/commands/mcp_bridge.py:97`) `def _build_parquet_query_parser()` - Return the argparse parser used by ``parquet_query``.
- `_build_threat_model_parser` (function, `cli/commands/mcp_bridge.py:116`) `def _build_threat_model_parser()` - Return the argparse parser used by ``threat_model``.
- `_build_playbook_run_parser` (function, `cli/commands/mcp_bridge.py:129`) `def _build_playbook_run_parser()` - Return the argparse parser used by ``playbook_run``.
- `McpBridgeCommandSet` (class, `cli/commands/mcp_bridge.py:143`) `class McpBridgeCommandSet(LazyOwnCommandSet)` - CLI shims exposing the documented MCP verbs to human operators.
- `do_auto_populate` (method, `cli/commands/mcp_bridge.py:151`) `def do_auto_populate(self, args)` - Parse the latest nmap XML scan and auto-populate payload context.
- `do_facts_show` (method, `cli/commands/mcp_bridge.py:261`) `def do_facts_show(self, args)` - Show structured facts extracted from nmap scans and tool output.
- `do_rag_query` (method, `cli/commands/mcp_bridge.py:286`) `def do_rag_query(self, args)` - Semantic search over session artefacts (scans, logs, notes).
- `do_parquet_query` (method, `cli/commands/mcp_bridge.py:316`) `def do_parquet_query(self, args)` - Query the parquet knowledge bases (GTFOBins, LOLBas, ATT&CK, sessions).
- `do_threat_model` (method, `cli/commands/mcp_bridge.py:378`) `def do_threat_model(self, args)` - Build or inspect the threat model derived from session events.
- `do_playbook_run` (method, `cli/commands/mcp_bridge.py:431`) `def do_playbook_run(self, args)` - Execute a generated YAML playbook step by step through the shell.
- `_executor` (function, `cli/commands/mcp_bridge.py:475`) `def _executor(command, host)`
- `do_auto_loop` (method, `cli/commands/mcp_bridge.py:489`) `def do_auto_loop(self, line)` - Run a goal through the single lazy orchestrator (auto_loop == lazy_loop).
- `do_session_state` (method, `cli/commands/mcp_bridge.py:516`) `def do_session_state(self, line)` - Alias of ``sitrep`` kept for MCP verb parity (lazyown_session_state).
- `do_campaign_sitrep` (method, `cli/commands/mcp_bridge.py:521`) `def do_campaign_sitrep(self, line)` - Alias of ``sitrep`` kept for MCP verb parity (lazyown_campaign_sitrep).

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 388
- Cross-boundary resolved imports (EXTRACTED): 195

## Connections

- [EXTRACTED] depends_on community 9 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 3 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/safe_exec.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [dataflow UNCHECKED_ALLOC] `modules/command_executor.py:224` `run_tee` `handle`: Result of allocator stored in `handle` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.

## Open Questions

- Why do 10 file(s) lack file-level docs (e.g. `gyms/docker/php2shell/src/info.php`)? What purpose do they serve?
- Can the cycle `modules/auto_registry.py` -> `modules/command_executor.py` be broken with an interface?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.46?

## Sources

- `2026-11-19_154944/jquery-1.11.3.min.js`
- `2026-11-19_162254/jquery-1.11.3.min.js`
- `2026-11-19_164345/jquery-1.11.3.min.js`
- `2026-11-19_170839/jquery-1.11.3.min.js`
- `cli/assign.py`
- `cli/commands/mcp_bridge.py`
- `cli/commands/session_ops.py`
- `cli/session_resumer.py`
- `cli/show.py`
- `cli/style.py`
- `core/process.py`
- `core/prompt.py`
- `core/safe_exec.py`
- `core/safe_subprocess.py`
- `gyms/docker/php2shell/src/info.php`
- `key.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/command_executor.py`
- `modules/dns_beacon.py`
- *... and 42 more*

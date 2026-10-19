# static/js

*Community 7 | 31 files | cohesion 0.51*

## Definition

This community groups 31 file(s) rooted at `static/js` with dominant language js (cohesion 0.51). Central symbols: `A`, `As`, `B`, `BUFFER`, `BackgroundSize`, `Be`, `BezierCurve`, `Bk`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

### `static/js` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |
| `static/js/chart.min.js` | js | utility | 88 | yes |
| `static/js/force-graph-1.43.5.min.js` | js | utility | 31 | yes |

### `contrib/legacy` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazybinenc.py` | py | utility | 2 | no |
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |
| `contrib/legacy/lazygptcli_unified.py` | py | utility | 29 | yes |
| `contrib/legacy/lazyproxy.py` | py | utility | 9 | no |

### `cli` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/show.py` | py | utility | 1 | yes |
| `cli/style.py` | py | utility | 4 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/colors.py` | py | utility | 3 | no |
| `modules/exp.c` | c | utility | 58 | yes |
| `modules/search.py` | py | utility | 0 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/process.py` | py | business_logic | 12 | yes |
| `core/prompt.py` | py | utility | 8 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/state.py` | py | utility | 0 | yes |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

*... and 11 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:36`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `format_payload` (function, `cli/show.py:14`) `def format_payload(params)` - Render ``params`` as a sorted, aligned ``key = value`` block.
- `style` (function, `cli/style.py:49`) `def style(token, theme)` - Return the Rich style string for a semantic token.
- `active_tokens` (function, `cli/style.py:68`) `def active_tokens(payload)` - Resolve every :data:`TOKEN_KEYS` entry for the payload's theme.
- `paint` (function, `cli/style.py:84`) `def paint(text, token, payload)` - Render ``text`` with the style of ``token`` for the active theme.
- `render_prompt` (function, `cli/style.py:98`) `def render_prompt(console, segments, payload)` - Print a themed prompt line composed of ``(text, token)`` pairs.
- `generate_key_iv` (function, `contrib/legacy/lazybinenc.py:12`) `def generate_key_iv(sessions_path)`
- `main` (function, `contrib/legacy/lazybinenc.py:54`) `def main()`
- `signal_handler` (function, `contrib/legacy/lazygptcli.py:66`) `def signal_handler(sig, frame)`
- `show_help` (function, `contrib/legacy/lazygptcli.py:73`) `def show_help(message)`
- `check_api_key` (function, `contrib/legacy/lazygptcli.py:77`) `def check_api_key()`
- `configure_logging` (function, `contrib/legacy/lazygptcli.py:83`) `def configure_logging(debug)`
- `parse_args` (function, `contrib/legacy/lazygptcli.py:87`) `def parse_args()`
- `create_complex_prompt` (function, `contrib/legacy/lazygptcli.py:94`) `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
- `execute_command` (function, `contrib/legacy/lazygptcli.py:108`) `def execute_command(command)`
- `load_knowledge_base` (function, `contrib/legacy/lazygptcli.py:118`) `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function, `contrib/legacy/lazygptcli.py:124`) `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function, `contrib/legacy/lazygptcli.py:128`) `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function, `contrib/legacy/lazygptcli.py:133`) `def get_relevant_knowledge(prompt)`
- `transform_knowledge_base` (function, `contrib/legacy/lazygptcli.py:141`) `def transform_knowledge_base(client)`
- `cleanup_temp_files` (function, `contrib/legacy/lazygptcli.py:164`) `def cleanup_temp_files()`
- `main` (function, `contrib/legacy/lazygptcli.py:177`) `def main()`
- `_ret_model` (function, `contrib/legacy/lazygptcli_unified.py:45`) `def _ret_model()`
- `truncate_message` (function, `contrib/legacy/lazygptcli_unified.py:53`) `def truncate_message(message, max_chars)`
- `_configure_logging` (function, `contrib/legacy/lazygptcli_unified.py:57`) `def _configure_logging(debug)`
- `_load_knowledge_base` (function, `contrib/legacy/lazygptcli_unified.py:62`) `def _load_knowledge_base(file_path)`
- `_save_knowledge_base` (function, `contrib/legacy/lazygptcli_unified.py:70`) `def _save_knowledge_base(knowledge_base, file_path)`
- `_add_to_knowledge_base` (function, `contrib/legacy/lazygptcli_unified.py:76`) `def _add_to_knowledge_base(prompt, response, file_path)`
- `_get_relevant_knowledge` (function, `contrib/legacy/lazygptcli_unified.py:82`) `def _get_relevant_knowledge(prompt, file_path)`
- `_transform_knowledge_base` (function, `contrib/legacy/lazygptcli_unified.py:95`) `def _transform_knowledge_base(client, kb_file, improved_file)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 236
- Cross-boundary resolved imports (EXTRACTED): 64

## Connections

- [EXTRACTED] depends_on community 7 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 9 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.

## Risks

- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyproxy.py:153` `handle_request` `server_socket`: Result of allocator stored in `server_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyproxy.py:184` `start_proxy` `proxy_socket`: Result of allocator stored in `proxy_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyseo.py:50` `results` `content`: Result of allocator stored in `content` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.

## Open Questions

- Why do 12 file(s) lack file-level docs (e.g. `contrib/legacy/lazybinenc.py`)? What purpose do they serve?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.51?

## Sources

- `cli/assign.py`
- `cli/show.py`
- `cli/style.py`
- `contrib/legacy/lazybinenc.py`
- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyproxy.py`
- `contrib/legacy/lazyseo.py`
- `core/process.py`
- `core/prompt.py`
- `key.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/colors.py`
- `modules/exp.c`
- `modules/search.py`
- `static/js/3d-force-graph-1.73.4.min.js`
- `static/js/bootstrap-4.5.2.min.js`
- `static/js/bootstrap-5.3.0.bundle.min.js`
- `static/js/chart.min.js`
- *... and 11 more*

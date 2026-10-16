# static/js

*Community 7 | 28 files | cohesion 0.45*

## Definition

This community groups 28 file(s) rooted at `static/js` with dominant language js (cohesion 0.45). Central symbols: `A`, `As`, `B`, `BUFFER`, `BackgroundSize`, `Be`, `BezierCurve`, `Bk`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

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

### `cli` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/show.py` | py | utility | 1 | yes |
| `cli/style.py` | py | utility | 4 | yes |

### `core` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/payload_schema.py` | py | utility | 27 | yes |
| `core/process.py` | py | business_logic | 12 | yes |
| `core/prompt.py` | py | utility | 8 | yes |

### `modules` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/exp.c` | c | utility | 58 | yes |
| `modules/search.py` | py | utility | 0 | yes |

### `tests` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_core_config.py` | py | testing | 19 | yes |
| `tests/test_payload_schema.py` | py | testing | 53 | yes |

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

*... and 8 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:36`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `format_payload` (function, `cli/show.py:14`) `def format_payload(params)` - Render ``params`` as a sorted, aligned ``key = value`` block.
- `style` (function, `cli/style.py:49`) `def style(token, theme)` - Return the Rich style string for a semantic token.
- `active_tokens` (function, `cli/style.py:68`) `def active_tokens(payload)` - Resolve every :data:`TOKEN_KEYS` entry for the payload's theme.
- `paint` (function, `cli/style.py:84`) `def paint(text, token, payload)` - Render ``text`` with the style of ``token`` for the active theme.
- `render_prompt` (function, `cli/style.py:98`) `def render_prompt(console, segments, payload)` - Print a themed prompt line composed of ``(text, token)`` pairs.
- `generate_key_iv` (function, `contrib/legacy/lazybinenc.py:12`) `def generate_key_iv(sessions_path)`
- `main` (function, `contrib/legacy/lazybinenc.py:54`) `def main()`
- `FieldKind` (class, `core/payload_schema.py:73`) `class FieldKind(StrEnum)` - Categorical type of a payload field used by validators and the wizard.
- `Severity` (class, `core/payload_schema.py:91`) `class Severity(StrEnum)` - Severity of a :class:`ValidationIssue`.
- `FieldSpec` (class, `core/payload_schema.py:100`) `class FieldSpec` - Declarative description of a payload field.
- `ValidationIssue` (class, `core/payload_schema.py:142`) `class ValidationIssue` - Structured outcome of a single validation check.
- `_validate_string` (function, `core/payload_schema.py:165`) `def _validate_string(value)`
- `_validate_int` (function, `core/payload_schema.py:171`) `def _validate_int(value)`
- `_validate_port` (function, `core/payload_schema.py:185`) `def _validate_port(value)`
- `_validate_bool` (function, `core/payload_schema.py:195`) `def _validate_bool(value)`
- `_validate_ip` (function, `core/payload_schema.py:212`) `def _validate_ip(value)`
- `_validate_hostname` (function, `core/payload_schema.py:220`) `def _validate_hostname(value)`
- `_validate_url` (function, `core/payload_schema.py:232`) `def _validate_url(value)`
- `_validate_path` (function, `core/payload_schema.py:240`) `def _validate_path(value)`
- `_validate_interface` (function, `core/payload_schema.py:246`) `def _validate_interface(value)`
- `_validate_hex` (function, `core/payload_schema.py:254`) `def _validate_hex(value)`
- `_validate_os_id` (function, `core/payload_schema.py:262`) `def _validate_os_id(value)`
- `_validate_json_blob` (function, `core/payload_schema.py:268`) `def _validate_json_blob(value)`
- `_validate_opaque` (function, `core/payload_schema.py:280`) `def _validate_opaque(_value)`
- `_coerce_int` (function, `core/payload_schema.py:301`) `def _coerce_int(raw)`
- `_coerce_bool` (function, `core/payload_schema.py:316`) `def _coerce_bool(raw)`
- `_spec` (function, `core/payload_schema.py:335`) `def _spec(name, kind, default, description)`
- `field_for` (function, `core/payload_schema.py:1582`) `def field_for(key)` - Return the :class:`FieldSpec` for ``key`` or ``None`` if it is unknown.
- `coerce_value` (function, `core/payload_schema.py:1587`) `def coerce_value(key, raw)` - Return ``raw`` coerced to the canonical type declared for ``key``.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 236
- Cross-boundary resolved imports (EXTRACTED): 84

## Connections

- [EXTRACTED] depends_on community 9 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 0 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/defaults.py imports cli/assign.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/process.py` via `subprocess` (5 hops)
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `contrib/legacy/lazybinenc.py`)? What purpose do they serve?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.45?

## Sources

- `cli/assign.py`
- `cli/show.py`
- `cli/style.py`
- `contrib/legacy/lazybinenc.py`
- `core/payload_schema.py`
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
- *... and 8 more*

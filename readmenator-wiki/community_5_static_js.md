# static/js

*Community 5 | 55 files | cohesion 0.42*

## Definition

This community groups 55 file(s) rooted at `static/js` with dominant language py (cohesion 0.42). Central symbols: `A`, `As`, `B`, `BUFFER`, `BackgroundSize`, `Be`, `BeaconConfig`, `BeaconConfigBuilder`. Core file: `static/js/html2pdf.bundle.min.js` (695 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

### `static/js` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |

### `tests` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_beacon_config_builder.py` | py | testing | 16 | yes |
| `tests/test_bof_registry.py` | py | testing | 51 | yes |

### `modules` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/auto_purple.py` | py | utility | 40 | yes |
| `modules/beacon_config_builder.py` | py | infrastructure | 14 | yes |
| `modules/bof_registry.py` | py | utility | 43 | yes |

### `cli/commands` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/bof_registry.py` | py | utility | 12 | yes |
| `cli/commands/c2_profile.py` | py | utility | 5 | yes |

### `core` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/config.py` | py | infrastructure | 17 | yes |
| `core/defaults.py` | py | utility | 8 | yes |

### `cli` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/session_resumer.py` | py | utility | 6 | yes |

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

### `lazyc2/blueprints` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/api.py` | py | presentation | 10 | yes |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

*... and 35 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:36`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `BofMarketplaceCommandSet` (class, `cli/commands/bof_registry.py:29`) `class BofMarketplaceCommandSet(LazyOwnCommandSet)` - BOF marketplace: search, install, info, list, run BOFs on beacons.
- `_ensure_staging_dir` (method, `cli/commands/bof_registry.py:36`) `def _ensure_staging_dir()` - Create and return the BOF staging directory path.
- `_find_bof_object` (method, `cli/commands/bof_registry.py:42`) `def _find_bof_object(bof_name)` - Find a compiled .o file for a BOF across all known source trees.
- `_stage_bof` (method, `cli/commands/bof_registry.py:71`) `def _stage_bof(self, bof_name)` - Find a compiled BOF object and stage it to sessions/temp_uploads/bofs/.
- `_queue_command_on_c2` (method, `cli/commands/bof_registry.py:89`) `def _queue_command_on_c2(self, client_id, command)` - Send a command to a connected beacon via the C2's issue_command endpoint.
- `do_bof_search` (method, `cli/commands/bof_registry.py:142`) `def do_bof_search(self, line)` - Search the BOF catalog by keyword.
- `do_bof_info` (method, `cli/commands/bof_registry.py:163`) `def do_bof_info(self, line)` - Show detailed information about a BOF.
- `do_bof_install` (method, `cli/commands/bof_registry.py:196`) `def do_bof_install(self, line)` - Install and compile a BOF, staging it for beacon delivery.
- `do_bof_run` (method, `cli/commands/bof_registry.py:226`) `def do_bof_run(self, line)` - Execute a BOF on a connected beacon.
- `do_bof_uninstall` (method, `cli/commands/bof_registry.py:267`) `def do_bof_uninstall(self, line)` - Uninstall a BOF and remove its staged file.
- `do_bof_list` (method, `cli/commands/bof_registry.py:289`) `def do_bof_list(self, line)` - List all installed and staged BOFs.
- `do_bof_catalog` (method, `cli/commands/bof_registry.py:321`) `def do_bof_catalog(self, line)` - List all BOFs available in the curated catalog.
- `C2ProfileCommandSet` (class, `cli/commands/c2_profile.py:18`) `class C2ProfileCommandSet(LazyOwnCommandSet)` - Extended C2 profile commands: TLS, DNS, SMB, WebSocket profiles.
- `do_c2_profiles` (method, `cli/commands/c2_profile.py:25`) `def do_c2_profiles(self, line)` - List all available C2 transport profiles.
- `do_c2_tls` (method, `cli/commands/c2_profile.py:50`) `def do_c2_tls(self, line)` - Display the current TLS C2 profile.
- `do_c2_dns` (method, `cli/commands/c2_profile.py:69`) `def do_c2_dns(self, line)` - Configure or display the DNS beacon profile.
- `do_c2_rotate` (method, `cli/commands/c2_profile.py:90`) `def do_c2_rotate(self, line)` - Rotate to the next C2 transport profile in the rotation queue.
- `DefaultsCommandSet` (class, `cli/commands/defaults.py:38`) `class DefaultsCommandSet(LazyOwnCommandSet)` - Inspect and override build-time default constants.
- `do_defaults` (method, `cli/commands/defaults.py:45`) `def do_defaults(self, line)` - Show or override build-time defaults (TOML + payload.json).
- `_show` (method, `cli/commands/defaults.py:60`) `def _show(self, section)` - Print TOML defaults alongside live payload values.
- `_set` (method, `cli/commands/defaults.py:77`) `def _set(self, name, value)` - Persist an override into payload.json via the assign path.
- `_build_exec_parser` (function, `cli/commands/purple_team.py:29`) `def _build_exec_parser()`
- `_build_test_parser` (function, `cli/commands/purple_team.py:67`) `def _build_test_parser()`
- `_build_config_parser` (function, `cli/commands/purple_team.py:92`) `def _build_config_parser()`
- `_build_history_parser` (function, `cli/commands/purple_team.py:106`) `def _build_history_parser()`
- `PurpleTeamCommandSet` (class, `cli/commands/purple_team.py:124`) `class PurpleTeamCommandSet(LazyOwnCommandSet)` - Purple team orchestration commands for the LazyOwn shell.
- `_get_loop` (method, `cli/commands/purple_team.py:130`) `def _get_loop(self)` - Build a PurpleTeamLoop from payload.json config.
- `do_purple_exec` (method, `cli/commands/purple_team.py:144`) `def do_purple_exec(self, line)` - Execute a red action and measure if LazyOwnBT detects it.
- `do_purple_test` (method, `cli/commands/purple_team.py:203`) `def do_purple_test(self, args)` - Test if LazyOwnBT would detect a command (no execution).

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 327
- Cross-boundary resolved imports (EXTRACTED): 171

## Connections

- [EXTRACTED] depends_on community 0 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/aliases.py imports core/config.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [layer strict] `tests/test_core_defaults.py` (testing) -> `lazyc2/blueprints/api.py` (presentation)
- [layer strict] `tests/test_security_hardening_v5.py` (testing) -> `lazyc2/blueprints/api.py` (presentation)
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

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `contrib/legacy/lazybinenc.py`)? What purpose do they serve?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.42?

## Sources

- `cli/assign.py`
- `cli/commands/bof_registry.py`
- `cli/commands/c2_profile.py`
- `cli/commands/defaults.py`
- `cli/commands/purple_team.py`
- `cli/commands/session_ops.py`
- `cli/commands/sleep_obfuscation.py`
- `cli/commands/socks_proxy.py`
- `cli/session_resumer.py`
- `cli/show.py`
- `cli/style.py`
- `contrib/legacy/lazybinenc.py`
- `core/config.py`
- `core/defaults.py`
- `core/payload_schema.py`
- `core/process.py`
- `core/prompt.py`
- `core/protocols.py`
- `key.py`
- `lazyc2/blueprints/api.py`
- *... and 35 more*

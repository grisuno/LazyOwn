# cli/commands: c2_profile_engine

*Community 8 | 26 files | cohesion 0.41*

## Definition

This community groups 26 file(s) rooted at `tests` with dominant language py (cohesion 0.41). Central symbols: `BeaconConfig`, `BeaconConfigBuilder`, `BofCatalog`, `BofCategory`, `BofEntry`, `BofMarketplace`, `BofMarketplaceCommandSet`, `BofPlatform`. Core file: `tests/test_c2_profile_engine.py` (63 symbols). Documented purpose: BOF marketplace CommandSet — Beacon Object File discovery, install, and execution.  Exposes ``modules/bof_registry`` through the LazyOwn CLI. Install compiles B.

## Files

### `tests` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_beacon_config_builder.py` | py | testing | 16 | yes |
| `tests/test_bof_registry.py` | py | testing | 51 | yes |
| `tests/test_c2_profile_engine.py` | py | testing | 63 | yes |
| `tests/test_command_allowlist.py` | py | testing | 14 | yes |
| `tests/test_command_allowlist_behavior.py` | py | testing | 3 | yes |

### `cli/commands` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/bof_registry.py` | py | utility | 12 | yes |
| `cli/commands/c2_profile.py` | py | utility | 5 | yes |
| `cli/commands/enum.py` | py | utility | 11 | yes |
| `cli/commands/sleep_obfuscation.py` | py | utility | 4 | yes |

### `modules` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_config_builder.py` | py | infrastructure | 14 | yes |
| `modules/bof_registry.py` | py | utility | 43 | yes |
| `modules/c2_profile_engine.py` | py | utility | 47 | yes |
| `modules/sleep_obfuscation.py` | py | utility | 28 | yes |

### `skills` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_claudemd.py` | py | utility | 8 | yes |
| `skills/lazyown_context.py` | py | utility | 11 | yes |
| `skills/lazyown_hooks.py` | py | utility | 14 | yes |
| `skills/lazyown_permissions.py` | py | utility | 16 | yes |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/scope_guard.py` | py | utility | 12 | yes |

### `lazyc2/security` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

*... and 6 more files in this community.*


## Key Symbols

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
- `EnumCommandSet` (class, `cli/commands/enum.py:31`) `class EnumCommandSet(LazyOwnCommandSet)` - Enumeration phase commands.
- `do_smbclient` (method, `cli/commands/enum.py:38`) `def do_smbclient(self, line)` - Interacts with SMB shares using the `smbclient` command to perform the following operations:
- `do_smbclient_impacket` (method, `cli/commands/enum.py:108`) `def do_smbclient_impacket(self, line)` - Interacts with SMB shares using the `smbclient` command to perform the following operations:
- `do_smbclient_py` (method, `cli/commands/enum.py:178`) `def do_smbclient_py(self, line)` - Interacts with SMB shares using the `smbclient.py` command to perform the following operations:
- `do_smbmap` (method, `cli/commands/enum.py:225`) `def do_smbmap(self, line)` - smbmap -H 10.10.10.3 [OPTIONS]
- `do_getnpusers` (method, `cli/commands/enum.py:345`) `def do_getnpusers(self, line)` - sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt
- `do_psexec` (method, `cli/commands/enum.py:390`) `def do_psexec(self, line)` - Executes the Impacket PSExec tool to attempt remote execution on the specified target.
- `do_psexec_py` (method, `cli/commands/enum.py:446`) `def do_psexec_py(self, line)` - Executes the Impacket PSExec tool to attempt remote execution on the specified target.
- `do_rpcdump` (method, `cli/commands/enum.py:502`) `def do_rpcdump(self, line)` - Executes the `rpcdump.py` script to dump RPC services from a target host.
- `do_enum4linux` (method, `cli/commands/enum.py:528`) `def do_enum4linux(self, line)` - Performs enumeration of information from a target Linux/Unix system using `enum4linux`.
- `do_rpcclient` (method, `cli/commands/enum.py:558`) `def do_rpcclient(self, line)` - Executes the `rpcclient` command to interact with a remote Windows system over RPC (Remote Procedure
- `SleepObfuscationCommandSet` (class, `cli/commands/sleep_obfuscation.py:16`) `class SleepObfuscationCommandSet(LazyOwnCommandSet)` - Sleep obfuscation technique manager.
- `do_sleep_list` (method, `cli/commands/sleep_obfuscation.py:23`) `def do_sleep_list(self, line)` - List available sleep obfuscation techniques.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 52
- Cross-boundary resolved imports (EXTRACTED): 51

## Connections

- [EXTRACTED] depends_on community 8 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 8 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports core/config.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`

## Open Questions

- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in cli/commands: c2_profile_engine changed?
- Should cli/commands: c2_profile_engine be split, given cohesion 0.41?

## Sources

- `cli/commands/bof_registry.py`
- `cli/commands/c2_profile.py`
- `cli/commands/enum.py`
- `cli/commands/sleep_obfuscation.py`
- `cli/commands/socks_proxy.py`
- `cli/scope_guard.py`
- `lazyc2/security/command_allowlist.py`
- `modules/beacon_config_builder.py`
- `modules/bof_registry.py`
- `modules/c2_profile_engine.py`
- `modules/sleep_obfuscation.py`
- `modules/socks_proxy.py`
- `skills/lazyown_claudemd.py`
- `skills/lazyown_context.py`
- `skills/lazyown_hooks.py`
- `skills/lazyown_permissions.py`
- `skills/lazyown_session.py`
- `skills/tests/test_harness_e2e.py`
- `tests/test_beacon_config_builder.py`
- `tests/test_bof_registry.py`
- *... and 6 more*

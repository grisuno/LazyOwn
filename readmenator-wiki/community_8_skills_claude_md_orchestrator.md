# skills/claude_md_orchestrator

*Community 8 | 61 files | cohesion 0.55*

## Definition

This community groups 61 file(s) rooted at `skills/claude_md_orchestrator` with dominant language py (cohesion 0.55). Central symbols: `AdvisoryLedger`, `AnalyzerResult`, `BddResult`, `BeaconConfig`, `BeaconConfigBuilder`, `BindAddressResolver`, `BofCatalog`, `BofCategory`. Core file: `tests/test_c2_profile_engine.py` (63 symbols). Documented purpose: BOF marketplace CommandSet — Beacon Object File discovery, staging and delivery.  Exposes :mod:`modules.bof_registry` and :mod:`modules.bof_delivery` through th.

## Files

### `skills/claude_md_orchestrator` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/claude_md_orchestrator/__init__.py` | py | utility | 0 | yes |
| `skills/claude_md_orchestrator/bdd_agent.py` | py | utility | 8 | yes |

### `tests` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_beacon_config_builder.py` | py | testing | 20 | yes |
| `tests/test_bof_admin.py` | py | testing | 27 | yes |

### `modules` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_config_builder.py` | py | infrastructure | 16 | yes |
| `modules/bof_admin.py` | py | utility | 14 | yes |

### `skills/hermes-lazyown` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |

### `modules/guardrails` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/guardrails/__init__.py` | py | utility | 0 | yes |
| `modules/guardrails/advisories.py` | py | utility | 15 | yes |

### `skills` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_claudemd.py` | py | utility | 8 | yes |
| `skills/lazyown_hooks.py` | py | utility | 14 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/bof_registry.py` | py | utility | 15 | yes |
| `cli/commands/enum.py` | py | utility | 11 | yes |

### `contrib/legacy` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `pwntomate.py` | py | utility | 3 | yes |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/scope_guard.py` | py | utility | 13 | yes |

### `lazyc2/security` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

*... and 41 more files in this community.*


## Key Symbols

- `BofMarketplaceCommandSet` (class, `cli/commands/bof_registry.py:44`) `class BofMarketplaceCommandSet(LazyOwnCommandSet)` - BOF marketplace: search, install, stage, deploy and run BOFs on beacons.
- `_ensure_staging_dir` (method, `cli/commands/bof_registry.py:51`) `def _ensure_staging_dir()` - Create and return the BOF staging directory path.
- `_stage_bof` (method, `cli/commands/bof_registry.py:56`) `def _stage_bof(self, bof_name)` - Stage a compiled BOF via the delivery service.
- `do_bof_search` (method, `cli/commands/bof_registry.py:87`) `def do_bof_search(self, line)` - Search the BOF catalog by keyword.
- `do_bof_info` (method, `cli/commands/bof_registry.py:108`) `def do_bof_info(self, line)` - Show detailed information about a BOF.
- `do_bof_install` (method, `cli/commands/bof_registry.py:143`) `def do_bof_install(self, line)` - Install and stage BOFs for beacon delivery.
- `do_bof_stage` (method, `cli/commands/bof_registry.py:171`) `def do_bof_stage(self, line)` - Stage a BOF artifact through its lazyaddon beacon client.
- `do_bof_run` (method, `cli/commands/bof_registry.py:191`) `def do_bof_run(self, line)` - Execute a BOF on a connected beacon.
- `do_bof_train` (method, `cli/commands/bof_registry.py:247`) `def do_bof_train(self, line)` - Run a sequence of BOFs over one beacon, awaiting each result.
- `do_bof_deploy` (method, `cli/commands/bof_registry.py:309`) `def do_bof_deploy(self, line)` - Deliver a staged beacon client onto a target and await check-in.
- `do_bof_beacons` (method, `cli/commands/bof_registry.py:358`) `def do_bof_beacons(self, line)` - List beacons currently seen by the C2.
- `do_bof_results` (method, `cli/commands/bof_registry.py:377`) `def do_bof_results(self, line)` - Show BOF execution history for one beacon.
- `do_bof_uninstall` (method, `cli/commands/bof_registry.py:409`) `def do_bof_uninstall(self, line)` - Uninstall a BOF and remove its staged file.
- `do_bof_list` (method, `cli/commands/bof_registry.py:431`) `def do_bof_list(self, line)` - List all installed and staged BOFs.
- `do_bof_catalog` (method, `cli/commands/bof_registry.py:463`) `def do_bof_catalog(self, line)` - List all BOFs available in the curated catalog.
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
- `ScopeMode` (class, `cli/scope_guard.py:90`) `class ScopeMode(StrEnum)` - Enforcement posture for the scope guard.
- `from_value` (method, `cli/scope_guard.py:105`) `def from_value(cls, value)` - Coerce an arbitrary payload value into a :class:`ScopeMode`.
- `ScopeDecision` (class, `cli/scope_guard.py:125`) `class ScopeDecision` - Outcome of a single scope evaluation.
- `build_offensive_commands` (function, `cli/scope_guard.py:147`) `def build_offensive_commands(command_categories)` - Select the command names whose category is offensive.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 118
- Cross-boundary resolved imports (EXTRACTED): 132

## Connections

- [EXTRACTED] depends_on community 6 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 8 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `skills/claude_md_orchestrator/parser.py` via `subprocess` (5 hops)
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [dataflow UNCHECKED_ALLOC] `modules/backdoor/server.c:19` `main` `sock`: Result of allocator stored in `sock` is never checked against NULL.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in skills/claude_md_orchestrator changed?
- Should skills/claude_md_orchestrator be split, given cohesion 0.55?

## Sources

- `cli/commands/bof_registry.py`
- `cli/commands/enum.py`
- `cli/scope_guard.py`
- `contrib/legacy/lazygalazy.py`
- `contrib/legacy/lazyhttpreverseshell.py`
- `lazyc2/security/command_allowlist.py`
- `modules/backdoor/server.c`
- `modules/beacon_config_builder.py`
- `modules/bof_admin.py`
- `modules/bof_delivery.py`
- `modules/bof_registry.py`
- `modules/c2_profile_engine.py`
- `modules/guardrails/__init__.py`
- `modules/guardrails/advisories.py`
- `modules/guardrails/budget.py`
- `modules/guardrails/checkpoints.py`
- `modules/guardrails/contracts.py`
- `modules/guardrails/harness.py`
- `modules/lazy_oob.py`
- `modules/lazyown_bprfuzzer.py`
- *... and 41 more*

# modules: bof_registry

*Community 10 | 48 files | cohesion 0.47*

## Definition

This community groups 48 file(s) rooted at `modules` with dominant language py (cohesion 0.47). Central symbols: `AdaptiveFallbackArbiter`, `AdvisoryLedger`, `Alternative`, `BeaconConfig`, `BeaconConfigBuilder`, `BofCatalog`, `BofCategory`, `BofDeliveryConfig`. Core file: `tests/test_c2_profile_engine.py` (63 symbols). Documented purpose: BOF marketplace CommandSet — Beacon Object File discovery, staging and delivery.  Exposes :mod:`modules.bof_registry` and :mod:`modules.bof_delivery` through th.

## Files

### `modules` (16 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_config_builder.py` | py | infrastructure | 16 | yes |
| `modules/bof_admin.py` | py | utility | 14 | yes |
| `modules/bof_delivery.py` | py | utility | 34 | yes |
| `modules/bof_registry.py` | py | utility | 51 | yes |

### `tests` (16 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_beacon_config_builder.py` | py | testing | 20 | yes |
| `tests/test_bof_admin.py` | py | testing | 27 | yes |
| `tests/test_bof_delivery.py` | py | testing | 26 | yes |
| `tests/test_bof_registry.py` | py | testing | 51 | yes |

### `modules/guardrails` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/guardrails/__init__.py` | py | utility | 0 | yes |
| `modules/guardrails/advisories.py` | py | utility | 15 | yes |
| `modules/guardrails/budget.py` | py | utility | 16 | yes |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/bof_registry.py` | py | utility | 19 | yes |
| `cli/commands/enum.py` | py | utility | 11 | yes |
| `cli/commands/lazy_adaptive.py` | py | utility | 4 | yes |

### `skills` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_claudemd.py` | py | utility | 8 | yes |
| `skills/lazyown_hooks.py` | py | utility | 14 | yes |
| `skills/lazyown_permissions.py` | py | utility | 16 | yes |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/scope_guard.py` | py | utility | 13 | yes |

### `lazyc2/security` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

*... and 28 more files in this community.*


## Key Symbols

- `BofMarketplaceCommandSet` (class, `cli/commands/bof_registry.py:44`) `class BofMarketplaceCommandSet(LazyOwnCommandSet)` - BOF marketplace: search, install, stage, deploy and run BOFs on beacons.
- `_ensure_staging_dir` (method, `cli/commands/bof_registry.py:51`) `def _ensure_staging_dir()` - Create and return the BOF staging directory path.
- `_stage_bof` (method, `cli/commands/bof_registry.py:56`) `def _stage_bof(self, bof_name)` - Stage a compiled BOF via the delivery service.
- `do_bof_search` (method, `cli/commands/bof_registry.py:87`) `def do_bof_search(self, line)` - Search the BOF catalog by keyword.
- `do_bof_info` (method, `cli/commands/bof_registry.py:108`) `def do_bof_info(self, line)` - Show detailed information about a BOF.
- `do_bof_install` (method, `cli/commands/bof_registry.py:143`) `def do_bof_install(self, line)` - Install and stage BOFs for beacon delivery.
- `do_bof_stage` (method, `cli/commands/bof_registry.py:171`) `def do_bof_stage(self, line)` - Stage a BOF artifact through its lazyaddon beacon client.
- `do_bof_run` (method, `cli/commands/bof_registry.py:191`) `def do_bof_run(self, line)` - Execute a BOF on a connected beacon.
- `do_bof_train` (method, `cli/commands/bof_registry.py:248`) `def do_bof_train(self, line)` - Run a sequence of BOFs over one beacon, awaiting each result.
- `do_bof_deploy` (method, `cli/commands/bof_registry.py:310`) `def do_bof_deploy(self, line)` - Deliver a staged beacon client onto a target and await check-in.
- `do_bof_beacons` (method, `cli/commands/bof_registry.py:359`) `def do_bof_beacons(self, line)` - List beacons currently seen by the C2.
- `do_bof_results` (method, `cli/commands/bof_registry.py:378`) `def do_bof_results(self, line)` - Show BOF execution history for one beacon.
- `do_bof_uninstall` (method, `cli/commands/bof_registry.py:410`) `def do_bof_uninstall(self, line)` - Uninstall a BOF and remove its staged file.
- `do_bof_list` (method, `cli/commands/bof_registry.py:432`) `def do_bof_list(self, line)` - List all installed and staged BOFs.
- `do_bof_catalog` (method, `cli/commands/bof_registry.py:464`) `def do_bof_catalog(self, line)` - List all BOFs available in the curated catalog.
- `_ensure_stage_token` (method, `cli/commands/bof_registry.py:499`) `def _ensure_stage_token(self)` - Return the payload staging token, generating one when absent.
- `_ensure_beacon_staged` (method, `cli/commands/bof_registry.py:524`) `def _ensure_beacon_staged(self)` - Stage the blacksandbeacon client when the /s/ copy is missing.
- `_build_fileless_oneliner` (method, `cli/commands/bof_registry.py:579`) `def _build_fileless_oneliner(self, stage_token)` - Build the fallback-chained fileless delivery one-liner.
- `do_bsb_stage` (method, `cli/commands/bof_registry.py:623`) `def do_bsb_stage(self, line)` - Stage the fileless BlackSandBeacon and print its delivery one-liner.
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 100
- Cross-boundary resolved imports (EXTRACTED): 115

## Connections

- [EXTRACTED] depends_on community 6 <-> 10 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/failure_verdict.py.
- [EXTRACTED] depends_on community 10 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 10 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports core/config.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/opsec_scorer.py` -> `core/config.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/opsec_scorer.py` be broken with an interface?
- What would break if the most connected file in modules: bof_registry changed?
- Should modules: bof_registry be split, given cohesion 0.47?

## Sources

- `cli/commands/bof_registry.py`
- `cli/commands/enum.py`
- `cli/commands/lazy_adaptive.py`
- `cli/commands/opsec_cleanup.py`
- `cli/scope_guard.py`
- `lazyc2/security/command_allowlist.py`
- `modules/beacon_config_builder.py`
- `modules/bof_admin.py`
- `modules/bof_delivery.py`
- `modules/bof_registry.py`
- `modules/bsb_compat.py`
- `modules/c2_profile_engine.py`
- `modules/failure_verdict.py`
- `modules/forensic_cleaner.py`
- `modules/guardrails/__init__.py`
- `modules/guardrails/advisories.py`
- `modules/guardrails/budget.py`
- `modules/guardrails/checkpoints.py`
- `modules/guardrails/contracts.py`
- `modules/guardrails/harness.py`
- *... and 28 more*

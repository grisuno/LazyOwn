# cli/commands

*Community 0 | 122 files | cohesion 0.62*

## Definition

This community groups 122 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.62). Central symbols: `ADCSCertipyWrapper`, `AWSAttackEngine`, `AWSConfig`, `AiCommandSet`, `AntiForensicsCommandSet`, `AppLockerBypassCommandSet`, `BackendAdapterSpec`, `BackendRegistrySpec`. Core file: `tests/test_improvements_spec.py` (160 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: Este archivo contiene la.

## Files

### `cli/commands` (56 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/_base.py` | py | utility | 7 | yes |
| `cli/commands/_dormancy.py` | py | data_access | 2 | yes |

### `modules` (35 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/aws_attacks.py` | py | utility | 11 | yes |
| `modules/bitm_engine.py` | py | utility | 18 | yes |

### `tests` (19 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_api_key_resolution.py` | py | testing | 9 | yes |
| `tests/test_categories.py` | py | testing | 47 | yes |

### `core` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/hardening.py` | py | utility | 14 | yes |
| `core/safe_exec.py` | py | utility | 12 | yes |
| `core/safe_subprocess.py` | py | business_logic | 7 | yes |

### `modules/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/legacy/lazygalazy.py` | py | utility | 7 | no |
| `modules/legacy/lazyhttpreverseshell.py` | py | presentation | 10 | no |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `banner.py` | py | utility | 3 | yes |
| `utils.py` | py | utility | 122 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/confirm.py` | py | utility | 2 | yes |
| `cli/registry.py` | py | utility | 2 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 3 | yes |

*... and 102 more files in this community.*


## Key Symbols

- `image_to_bash` (function, `banner.py:25`) `def image_to_bash(image_path, image_res)`
- `list_png_files` (function, `banner.py:47`) `def list_png_files()`
- `main` (function, `banner.py:56`) `def main()`
- `extract_flag` (function, `cli/commands/_base.py:34`) `def extract_flag(args, flag)` - Extract ``--flag <value>`` pair shared by CommandSets.
- `LazyOwnCommandSet` (class, `cli/commands/_base.py:51`) `class LazyOwnCommandSet(CommandSet)` - Base class for every phase ``CommandSet`` defined under ``cli.commands``.
- `_resolve_shell` (method, `cli/commands/_base.py:65`) `def _resolve_shell(self)` - Return the bound parent shell, or ``None`` before registration.
- `params` (method, `cli/commands/_base.py:86`) `def params(self)` - Return the live ``params`` dict owned by the parent shell.
- `payload` (method, `cli/commands/_base.py:97`) `def payload(self)` - Return the parent shell's ``Config`` wrapper when available.
- `__getattr__` (method, `cli/commands/_base.py:110`) `def __getattr__(self, name)` - Forward unknown attribute access to the bound shell or utils.
- `__setattr__` (method, `cli/commands/_base.py:162`) `def __setattr__(self, name, value)` - Forward prompt attribute writes to the bound shell.
- `PendingCommandSet` (class, `cli/commands/_dormancy.py:30`) `class PendingCommandSet(LazyOwnCommandSet)` - Base class for migrated-but-not-yet-active phase command sets.
- `is_pending` (method, `cli/commands/_dormancy.py:52`) `def is_pending(cs_class)` - Return ``True`` when ``cs_class`` is flagged as a pending migration.
- `AiCommandSet` (class, `cli/commands/ai.py:70`) `class AiCommandSet(LazyOwnCommandSet)` - Pending phase module for the Artificial Intelligence commands.
- `do_ask` (method, `cli/commands/ai.py:77`) `def do_ask(self, line)` - Ask the AI a question with current session context pre-loaded.
- `do_groq` (method, `cli/commands/ai.py:146`) `def do_groq(self, line)` - Generate a single-line command through the Groq backend.
- `do_ai_playbook` (method, `cli/commands/ai.py:177`) `def do_ai_playbook(self, line)` - Generate an offensive playbook from Nmap CSV + KB + Ollama.
- `do_ai_toggle` (method, `cli/commands/ai.py:284`) `def do_ai_toggle(self, _arg)` - Toggle the in-process AI assistant on or off.
- `do_llm_budget` (method, `cli/commands/ai.py:301`) `def do_llm_budget(self, line)` - Show the LLM daily cost budget, per call token cap, and current spend.
- `AntiForensicsCommandSet` (class, `cli/commands/anti_forensics.py:29`) `class AntiForensicsCommandSet(LazyOwnCommandSet)` - Anti-forensics operations for post-exploitation cleanup.
- `do_wipe_logs` (method, `cli/commands/anti_forensics.py:36`) `def do_wipe_logs(self, line)` - Clear system log files on the remote target.
- `do_wipe_timeline` (method, `cli/commands/anti_forensics.py:97`) `def do_wipe_timeline(self, line)` - Scrub file timestamps and shell history on the target.
- `do_shred` (method, `cli/commands/anti_forensics.py:140`) `def do_shred(self, line)` - Securely delete files by overwriting before removal.
- `do_wipe_free` (method, `cli/commands/anti_forensics.py:190`) `def do_wipe_free(self, line)` - Wipe free disk space to prevent forensic file recovery.
- `do_clean_ad` (method, `cli/commands/anti_forensics.py:223`) `def do_clean_ad(self, line)` - Clear Active Directory event logs and cached Kerberos tickets.
- `do_cover_tracks` (method, `cli/commands/anti_forensics.py:280`) `def do_cover_tracks(self, line)` - Run all anti-forensics operations in sequence.
- `_extract_flag` (method, `cli/commands/anti_forensics.py:314`) `def _extract_flag(args, flag)` - Extract a ``--flag <value>`` pair from a list of arguments.
- `AppLockerBypassCommandSet` (class, `cli/commands/applocker_bypass.py:99`) `class AppLockerBypassCommandSet(LazyOwnCommandSet)` - AppLocker and WDAC bypass payload generators.
- `_get_lh` (method, `cli/commands/applocker_bypass.py:105`) `def _get_lh(self)`
- `do_applocker_installutil` (method, `cli/commands/applocker_bypass.py:109`) `def do_applocker_installutil(self, line)` - Generate an InstallUtil.exe AppLocker bypass payload.
- `do_applocker_msbuild` (method, `cli/commands/applocker_bypass.py:146`) `def do_applocker_msbuild(self, line)` - Generate an MSBuild.exe AppLocker bypass payload.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 364
- Cross-boundary resolved imports (EXTRACTED): 198

## Connections

- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/registry.py.
- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/active_directory.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_adapter.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/audit.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/exploit_migrated.py imports modules/exploit_recommender.py.
- [EXTRACTED] depends_on community 5 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/payload_arsenal.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/safe_subprocess.py` via `subprocess` (5 hops)
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [layer strict] `tests/test_daemon_ctl_command_set.py` (testing) -> `cli/commands/misc_migrated.py` (presentation)
- [layer strict] `tests/test_encoding_command_set.py` (testing) -> `cli/commands/misc_migrated.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/misc_migrated.py` (presentation)
- [layer strict] `tests/test_improvements_spec.py` (testing) -> `cli/status_bar.py` (presentation)
- [layer strict] `tests/test_improvements_spec.py` (testing) -> `cli/status_bar.py` (presentation)

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `modules/backdoor/server.c`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.62?

## Sources

- `banner.py`
- `cli/commands/__init__.py`
- `cli/commands/_base.py`
- `cli/commands/_dormancy.py`
- `cli/commands/ai.py`
- `cli/commands/anti_forensics.py`
- `cli/commands/applocker_bypass.py`
- `cli/commands/bitm.py`
- `cli/commands/c2_profile.py`
- `cli/commands/caldera.py`
- `cli/commands/campaign.py`
- `cli/commands/catalog.py`
- `cli/commands/cicd.py`
- `cli/commands/cli_auth.py`
- `cli/commands/cloud.py`
- `cli/commands/cloud_attacks.py`
- `cli/commands/collaboration.py`
- `cli/commands/command_and_control.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/commands/cred.py`
- *... and 102 more*

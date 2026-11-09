# modules/guardrails

*Community 11 | 22 files | cohesion 0.40*

## Definition

This community groups 22 file(s) rooted at `modules/guardrails` with dominant language py (cohesion 0.40). Central symbols: `AdvisoryLedger`, `BofCatalog`, `BofCategory`, `BofEntry`, `BofMarketplace`, `BofPlatform`, `BofRegistry`, `BofValidator`. Core file: `tests/test_socks_proxy.py` (52 symbols). Documented purpose: Enumeration command set.  Service enumeration commands: SMB, RPC, LDAP quick checks, and related impacket tools..

## Files

### `modules/guardrails` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/guardrails/__init__.py` | py | utility | 0 | yes |
| `modules/guardrails/advisories.py` | py | utility | 15 | yes |
| `modules/guardrails/budget.py` | py | utility | 16 | yes |
| `modules/guardrails/checkpoints.py` | py | utility | 7 | yes |
| `modules/guardrails/contracts.py` | py | utility | 10 | yes |

### `tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_bof_registry.py` | py | testing | 51 | yes |
| `tests/test_command_allowlist.py` | py | testing | 14 | yes |
| `tests/test_command_allowlist_behavior.py` | py | testing | 3 | yes |
| `tests/test_scope_guard.py` | py | testing | 46 | yes |
| `tests/test_sleep_obfuscation.py` | py | testing | 41 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/bof_registry.py` | py | utility | 43 | yes |
| `modules/sleep_obfuscation.py` | py | utility | 28 | yes |
| `modules/socks_proxy.py` | py | utility | 31 | yes |

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

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/enum.py` | py | utility | 11 | yes |

### `lazyc2/security` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

*... and 2 more files in this community.*


## Key Symbols

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
- `normalize_scope` (function, `cli/scope_guard.py:163`) `def normalize_scope(entries)` - Coerce a scope specification into a tuple of entry strings.
- `_parse_ip` (function, `cli/scope_guard.py:195`) `def _parse_ip(value)`
- `_parse_network` (function, `cli/scope_guard.py:202`) `def _parse_network(value)`
- `_hostname_match` (function, `cli/scope_guard.py:209`) `def _hostname_match(target, entry)`
- `target_in_scope` (function, `cli/scope_guard.py:218`) `def target_in_scope(target, entries)` - Return whether *target* falls within any of the scope *entries*.
- `target_in_deny` (function, `cli/scope_guard.py:254`) `def target_in_deny(target, entries)` - Return whether *target* is explicitly denied.
- `ScopeGuard` (class, `cli/scope_guard.py:271`) `class ScopeGuard` - Decides whether an offensive command may run against the active target.
- `__init__` (method, `cli/scope_guard.py:280`) `def __init__(self, scope_entries, mode, is_offensive, deny_entries)` - Initialise the guard.
- `evaluate` (method, `cli/scope_guard.py:304`) `def evaluate(self, command, target)` - Evaluate a single command against the active target.
- `CommandRejectionReason` (class, `lazyc2/security/command_allowlist.py:36`) `class CommandRejectionReason(StrEnum)` - Why a command was rejected by :class:`CommandAllowlist`.
- `CommandDecision` (class, `lazyc2/security/command_allowlist.py:48`) `class CommandDecision` - The outcome of a single command allowlist check.
- `to_dict` (method, `lazyc2/security/command_allowlist.py:61`) `def to_dict(self)` - Return a JSON-serializable dict for the audit log.
- `CommandAllowlist` (class, `lazyc2/security/command_allowlist.py:70`) `class CommandAllowlist` - Allowlist gate for the ``/api/run`` endpoint.
- `__init__` (method, `lazyc2/security/command_allowlist.py:82`) `def __init__(self, allowed, audit_log_path)`
- `allowed` (method, `lazyc2/security/command_allowlist.py:94`) `def allowed(self)` - Return the immutable set of allowed first tokens (lowercased).

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 33
- Cross-boundary resolved imports (EXTRACTED): 64

## Connections

- [EXTRACTED] depends_on community 6 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 5 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports modules/bof_registry.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`

## Open Questions

- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in modules/guardrails changed?
- Should modules/guardrails be split, given cohesion 0.40?

## Sources

- `cli/commands/enum.py`
- `cli/scope_guard.py`
- `lazyc2/security/command_allowlist.py`
- `modules/bof_registry.py`
- `modules/guardrails/__init__.py`
- `modules/guardrails/advisories.py`
- `modules/guardrails/budget.py`
- `modules/guardrails/checkpoints.py`
- `modules/guardrails/contracts.py`
- `modules/guardrails/harness.py`
- `modules/sleep_obfuscation.py`
- `modules/socks_proxy.py`
- `skills/lazyown_claudemd.py`
- `skills/lazyown_hooks.py`
- `skills/lazyown_permissions.py`
- `skills/tests/test_harness_e2e.py`
- `tests/test_bof_registry.py`
- `tests/test_command_allowlist.py`
- `tests/test_command_allowlist_behavior.py`
- `tests/test_scope_guard.py`
- *... and 2 more*

# modules: opsec_scorer

*Community 8 | 27 files | cohesion 0.46*

## Definition

This community groups 27 file(s) rooted at `modules` with dominant language py (cohesion 0.46). Central symbols: `CheckpointSerializer`, `CompactionResult`, `CompactionStrategy`, `ConfigBridge`, `ConfigBridgeError`, `ConfigKeys`, `CrackResult`, `DefaultCompaction`. Core file: `tests/test_killchain_unified_v2.py` (43 symbols). Documented purpose: OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory, network.  Provides: opsec_score             — Real-time OPSEC risk assess.

## Files

### `modules` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/forensic_cleaner.py` | py | utility | 8 | yes |
| `modules/hash_cracker.py` | py | utility | 17 | yes |
| `modules/kill_chain_viz.py` | py | utility | 5 | yes |
| `modules/killchain.py` | py | utility | 21 | yes |
| `modules/log_tamper.py` | py | utility | 9 | yes |
| `modules/memory_cleaner.py` | py | utility | 7 | yes |

### `skills/hermes-lazyown` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |
| `skills/hermes-lazyown/constants.py` | py | utility | 15 | yes |
| `skills/hermes-lazyown/executor.py` | py | utility | 13 | yes |
| `skills/hermes-lazyown/hermes_sync.py` | py | utility | 14 | yes |

### `tests` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_credential_vault.py` | py | testing | 16 | yes |
| `tests/test_hash_cracker.py` | py | testing | 22 | yes |
| `tests/test_killchain.py` | py | testing | 9 | yes |
| `tests/test_killchain_snapshot.py` | py | testing | 12 | yes |
| `tests/test_killchain_unified_v2.py` | py | testing | 43 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/opsec_cleanup.py` | py | utility | 9 | yes |
| `cli/commands/security.py` | py | utility | 8 | yes |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/killchain.py` | py | utility | 4 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/credential_vault.py` | py | utility | 8 | yes |

*... and 7 more files in this community.*


## Key Symbols

- `OpsecCleanupCommandSet` (class, `cli/commands/opsec_cleanup.py:19`) `class OpsecCleanupCommandSet(LazyOwnCommandSet)` - OPSEC scoring, log tampering, forensic cleaning, timestomping, memory/network OPSEC.
- `do_opsec_score` (method, `cli/commands/opsec_cleanup.py:25`) `def do_opsec_score(self, line)` - Real-time OPSEC risk assessment with contextual action gating (v2).
- `do_log_tamper` (method, `cli/commands/opsec_cleanup.py:97`) `def do_log_tamper(self, line)` - Cross-platform log clearing commands.
- `do_forensic_clean` (method, `cli/commands/opsec_cleanup.py:162`) `def do_forensic_clean(self, line)` - Clean forensic artifacts — Prefetch, Shimcache, Amcache, Jump Lists, etc.
- `do_timestomp` (method, `cli/commands/opsec_cleanup.py:219`) `def do_timestomp(self, line)` - Manipulate file MACB timestamps to evade forensic timeline analysis.
- `do_memory_clean` (method, `cli/commands/opsec_cleanup.py:288`) `def do_memory_clean(self, line)` - Clean memory artifacts — Kerberos tickets, clipboard, env vars, credentials.
- `do_network_opsec` (method, `cli/commands/opsec_cleanup.py:342`) `def do_network_opsec(self, line)` - Network OPSEC — proxy chains, DoH, canary detection, traffic analysis.
- `do_auditd_disable` (method, `cli/commands/opsec_cleanup.py:445`) `def do_auditd_disable(self, line)` - Generate commands to disable Linux auditd.
- `do_sysmon_disable` (method, `cli/commands/opsec_cleanup.py:468`) `def do_sysmon_disable(self, line)` - Generate commands to disable Windows Sysmon.
- `SecurityCommandSet` (class, `cli/commands/security.py:20`) `class SecurityCommandSet(LazyOwnCommandSet)` - OPSEC scoring, credential vault, and hash cracking commands.
- `do_opsec` (method, `cli/commands/security.py:26`) `def do_opsec(self, line)` - Score OPSEC risk for a LazyOwn command before execution.
- `do_seal_credentials` (method, `cli/commands/security.py:106`) `def do_seal_credentials(self, _line)` - Encrypt all sensitive values in payload.json using AES-256-GCM.
- `do_rotate_aes` (method, `cli/commands/security.py:127`) `def do_rotate_aes(self, _line)` - Generate a new AES key and re-encrypt all sealed credentials.
- `do_unseal_credentials` (method, `cli/commands/security.py:150`) `def do_unseal_credentials(self, _line)` - Decrypt sealed credential values in payload.json for inspection.
- `do_crack_hashes` (method, `cli/commands/security.py:170`) `def do_crack_hashes(self, line)` - Crack password hashes from a file using John the Ripper or Hashcat.
- `complete_opsec` (method, `cli/commands/security.py:267`) `def complete_opsec(self, text, line, begidx, endidx)`
- `complete_crack_hashes` (method, `cli/commands/security.py:276`) `def complete_crack_hashes(self, text, line, begidx, endidx)`
- `PhaseProgress` (class, `cli/killchain.py:29`) `class PhaseProgress` - Computed progress for a single kill-chain phase.
- `_phase_from_event` (function, `cli/killchain.py:48`) `def _phase_from_event(event)` - Return the phase an event belongs to, empty string if absent.
- `_detect_current_phase` (function, `cli/killchain.py:58`) `def _detect_current_phase(events, world, phase_keys)` - Resolve the active phase from events, falling back to the world model.
- `compute_killchain` (function, `cli/killchain.py:83`) `def compute_killchain(events, world, phases)` - Compute kill-chain progress from daemon events and the world model.
- `check_dangerous_defaults` (function, `core/credential_vault.py:63`) `def check_dangerous_defaults(payload)` - Scan payload for unchanged default credential values.
- `_get_aes_key` (function, `core/credential_vault.py:79`) `def _get_aes_key(payload)` - Resolve the AES key from payload, disk, or generate fresh.
- `seal_value` (function, `core/credential_vault.py:93`) `def seal_value(plaintext, key)` - Encrypt a single credential value.
- `unseal_value` (function, `core/credential_vault.py:112`) `def unseal_value(sealed, key)` - Decrypt a sealed credential value.
- `seal_payload` (function, `core/credential_vault.py:141`) `def seal_payload(payload, key)` - Return a copy of ``payload`` with all sensitive values encrypted.
- `unseal_payload` (function, `core/credential_vault.py:164`) `def unseal_payload(payload, key)` - Return a copy of ``payload`` with all sealed values decrypted.
- `rotate_aes_key` (function, `core/credential_vault.py:186`) `def rotate_aes_key(payload, current_key)` - Generate a new AES key, re-encrypt all sealed values under it.
- `generate_secure_defaults` (function, `core/credential_vault.py:215`) `def generate_secure_defaults()` - Generate cryptographically random default values for sensitive keys.
- `ForensicCleanerConfig` (class, `modules/forensic_cleaner.py:23`) `class ForensicCleanerConfig` - Configuration for forensic artifact cleaning.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 38
- Cross-boundary resolved imports (EXTRACTED): 81

## Connections

- [EXTRACTED] depends_on community 11 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: opsec_scorer changed?
- Should modules: opsec_scorer be split, given cohesion 0.46?

## Sources

- `cli/commands/opsec_cleanup.py`
- `cli/commands/security.py`
- `cli/killchain.py`
- `core/credential_vault.py`
- `modules/forensic_cleaner.py`
- `modules/hash_cracker.py`
- `modules/kill_chain_viz.py`
- `modules/killchain.py`
- `modules/log_tamper.py`
- `modules/memory_cleaner.py`
- `modules/network_opsec.py`
- `modules/opsec_scorer.py`
- `modules/timestomper.py`
- `skills/hermes-lazyown/claudemd_rules.py`
- `skills/hermes-lazyown/config_bridge.py`
- `skills/hermes-lazyown/constants.py`
- `skills/hermes-lazyown/executor.py`
- `skills/hermes-lazyown/hermes_sync.py`
- `skills/hermes-lazyown/mcp_server.py`
- `skills/hermes-lazyown/output_compactor.py`
- *... and 7 more*
